from flask import Flask, render_template, request, redirect
import sqlite3
from flask import send_file
import csv
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "portfolio_secret_key"

def init_db():
    conn = sqlite3.connect("portfolio.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stocks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        qty INTEGER,
        buy_price REAL,
        current_price REAL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()
@app.route("/export")
def export():

    conn = sqlite3.connect("portfolio.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM stocks")
    rows = cur.fetchall()

    conn.close()

    with open("portfolio_report.csv","w",newline="") as f:

        writer = csv.writer(f)

        writer.writerow(
            ["ID","Name","Qty","Buy Price","Current Price"]
        )

        writer.writerows(rows)

    return send_file(
        "portfolio_report.csv",
        as_attachment=True
    )
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("portfolio.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("portfolio.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            session["user"] = username
            return redirect("/")

    return render_template("login.html")

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("portfolio.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM stocks")
    rows = cur.fetchall()

    conn.close()

    stocks = []

    total_investment = 0
    current_value = 0

    for row in rows:

        stock = {
            "id": row[0],
            "name": row[1],
            "qty": row[2],
            "buy_price": row[3],
            "current_price": row[4]
        }

        stock["profit"] = (
            stock["current_price"] - stock["buy_price"]
        ) * stock["qty"]

        total_investment += stock["buy_price"] * stock["qty"]
        current_value += stock["current_price"] * stock["qty"]

        stocks.append(stock)

    profit = current_value - total_investment
    

    return render_template(
        "index.html",
        stocks=stocks,
        total_investment=round(total_investment, 2),
        current_value=round(current_value, 2),
        profit=round(profit, 2)
    )

@app.route("/add", methods=["POST"])
def add():

    name = request.form["name"]
    qty = request.form["qty"]
    buy_price = request.form["buy_price"]
    current_price = request.form["current_price"]

    conn = sqlite3.connect("portfolio.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO stocks
    (name, qty, buy_price, current_price)
    VALUES (?, ?, ?, ?)
    """, (name, qty, buy_price, current_price))

    conn.commit()
    conn.close()

    return redirect("/")
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("portfolio.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM stocks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)