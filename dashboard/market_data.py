import yfinance as yf
from django.core.cache import cache


MARKET_TICKERS = ["MSFT", "AAPL", "NVDA", "IEF", "MC.PA", "NESN.SW"]


def get_market_snapshot():
    cache_key = "market_snapshot"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    market_rows = []

    for ticker in MARKET_TICKERS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info

            last_price = info.get("last_price")
            previous_close = info.get("previous_close")

            if last_price and previous_close:
                change = last_price - previous_close
                change_percent = (change / previous_close) * 100
            else:
                change = None
                change_percent = None

            market_rows.append({
                "ticker": ticker,
                "last_price": round(last_price, 2) if last_price else "N/A",
                "previous_close": round(previous_close, 2) if previous_close else "N/A",
                "change": round(change, 2) if change is not None else "N/A",
                "change_percent": round(change_percent, 2) if change_percent is not None else "N/A",
            })

        except Exception:
            market_rows.append({
                "ticker": ticker,
                "last_price": "Unavailable",
                "previous_close": "Unavailable",
                "change": "Unavailable",
                "change_percent": "Unavailable",
            })

    cache.set(cache_key, market_rows, 300)
    return market_rows