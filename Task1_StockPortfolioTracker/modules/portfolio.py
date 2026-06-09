from modules.stock_data import STOCK_PRICES
from modules.validator import validate_stock, validate_quantity


def add_stocks():
    portfolio = {}

    while True:
        stock = input(
            "\nEnter Stock Symbol (or 'done' to finish): "
        ).upper()

        if stock == "DONE":
            break

        if not validate_stock(stock):
            print("❌ Invalid Stock Symbol")
            continue

        quantity = input("Enter Quantity: ")

        if not validate_quantity(quantity):
            print("❌ Quantity must be a positive number")
            continue

        quantity = int(quantity)

        portfolio[stock] = portfolio.get(stock, 0) + quantity

        print("✅ Stock Added Successfully")

    return portfolio


def calculate_portfolio(portfolio):
    report = []
    total_value = 0

    for stock, quantity in portfolio.items():
        price = STOCK_PRICES[stock]
        investment = quantity * price

        report.append({
            "stock": stock,
            "quantity": quantity,
            "price": price,
            "investment": investment
        })

        total_value += investment

    return report, total_value