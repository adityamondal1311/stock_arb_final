def compare(nse_price, bse_price):
    if nse_price is None or bse_price is None:
        return None
    return round(nse_price - bse_price, 2)
