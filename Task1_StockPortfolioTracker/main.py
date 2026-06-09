from modules.stock_data import STOCK_PRICES
from modules.portfolio import (
    add_stocks,
    calculate_portfolio
)
from modules.report import (
    display_report,
    save_to_csv,
    save_to_txt
)


def show_available_stocks():

    print("\nAvailable Stocks")
    print("-" * 30)

    for stock, price in STOCK_PRICES.items():
        print(f"{stock:<10} : ${price}")

    print("-" * 30)


def main():

    print("=" * 60)
    print("        STOCK PORTFOLIO TRACKER")
    print("=" * 60)

    show_available_stocks()

    portfolio = add_stocks()

    if not portfolio:
        print("\n⚠ No stocks were added.")
        return

    report, total_value = calculate_portfolio(
        portfolio
    )

    display_report(report, total_value)

    choice = input(
        "\nSave report? (y/n): "
    ).lower()

    if choice == "y":
        save_to_csv(report, total_value)
        save_to_txt(report, total_value)

    print("\nThank you for using the tracker.")


if __name__ == "__main__":
    main()