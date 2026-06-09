from modules.stock_data import STOCK_PRICES


def validate_stock(stock):
    return stock.upper() in STOCK_PRICES


def validate_quantity(quantity):
    try:
        quantity = int(quantity)
        return quantity > 0
    except ValueError:
        return False