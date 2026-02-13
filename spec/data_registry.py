import os

DATA_MAP = {
    "VALID_USERNAME": os.getenv("VALID_USERNAME"),
    "VALID_PASSWORD": os.getenv("VALID_PASSWORD"),
    "INVALID_USERNAME": "bad_user",
    "INVALID_PASSWORD": "bad_pass",
    "PRODUCT_TO_VIEW": "ADIDAS",
    "MIN_PRICE_FILTER": "10000",
    "MAX_PRICE_FILTER": "15000",
    "SEARCH_TEXT": "ADIDAS",
    "HOUSEHOLD_FILTER": "household",
    "CART_ITEMS": ("ZARA", "IPHONE"),
    "CART_ICON_TEXT": "Cart"
}
