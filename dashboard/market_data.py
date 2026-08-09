import yfinance as yf
# This imports the yfinance library, which allows the project to request market data from Yahoo Finance.
# In this app, I use it to show a market snapshot on the dashboard.
from django.core.cache import cache
# This imports Django's cache system.
# The cache helps store market data temporarily so the app does not request Yahoo Finance data every time the page reloads.


MARKET_TICKERS = ["MSFT", "AAPL", "NVDA", "IEF", "MC.PA", "NESN.SW"]
# This list stores the ticker symbols that will appear in the dashboard market snapshot.
# MSFT, AAPL and NVDA are US technology stocks.
# IEF is a bond ETF.
# MC.PA is LVMH listed in Paris.
# NESN.SW is Nestlé listed in Switzerland.
# This makes the dashboard more finance-related and connects the project to portfolio review ideas such as diversification and market monitoring.
def get_market_snapshot():
    # This function collects market information and returns it as a list of dictionaries.
    # The dashboard view can call this function and then send the returned data to the HTML template.
    # This keeps the external market-data logic separate from views.py, which makes the Django project more modular.
    cache_key = "market_snapshot"
    # This creates a cache name for the market data.
    # Django uses this key to remember where the saved market snapshot is stored temporarily.
    cached_data = cache.get(cache_key)
    # This checks whether market data has already been saved in the cache.
    # If cached data exists, the app can use it instead of contacting Yahoo Finance again.
    if cached_data:
        # This checks if Django found existing cached market data.
        return cached_data
        # This returns the cached market data immediately.
        # This makes the dashboard faster and reduces repeated requests to Yahoo Finance.
    market_rows = []
    # This creates an empty list.
    # Each ticker's market data will be added to this list as one dictionary.
    # Later, the dashboard template loops through this list using {% for row in market_rows %}.
    for ticker in MARKET_TICKERS:
        # This loop goes through each ticker symbol in the MARKET_TICKERS list one at a time.
        # For example, the first loop checks MSFT, then AAPL, then NVDA, and so on.
        try:
            # The try block is used because external data can fail.
            # Yahoo Finance might be unavailable, the internet might fail, or one ticker might not return data.
            # Using try means the whole dashboard will not crash if one ticker has a problem.
            stock = yf.Ticker(ticker)
            # This creates a yfinance Ticker object for the current ticker symbol.
            # For example, if ticker is "MSFT", this asks yfinance to prepare Microsoft market data.
            history = stock.history(period="5d")
            # This asks Yahoo Finance for the last 5 days of price history.
            # I use 5 days because weekends and market holidays can mean there is no trading data for some dates.
            if history.empty or len(history) < 2:
                # This checks whether Yahoo Finance returned enough data.
                # We need at least two closing prices: one latest close and one previous trading day close.
                market_rows.append({
                    # This adds a fallback row to the market_rows list if data is missing.
                    "ticker": ticker,
                    # This still displays the ticker symbol even if the prices are missing.
                    "current_price": "N/A",
                    # This shows N/A when the current price cannot be calculated.
                    "last_price": "N/A",
                    # This shows N/A when the last available price is missing.
                    "previous_trading_day_close": "N/A",
                    # This shows N/A when there is no previous close available.
                    "change_percent": "N/A",
                    # This shows N/A when the percentage change cannot be calculated.
                })
                continue
                # This skips the rest of the loop for this ticker and moves to the next ticker.
                # It prevents Python from trying to calculate prices from missing data.
            current_price = float(history["Close"].iloc[-1])
            # This gets the most recent closing price from the history table.
            # iloc[-1] means the last row in the data.
            # float() converts the value into a normal Python number.
            previous_close = float(history["Close"].iloc[-2])
            # This gets the previous trading day's closing price.
            # iloc[-2] means the second-last row in the data.
            change_percent = ((current_price - previous_close) / previous_close) * 100
            # This calculates the percentage change from the previous trading day to the latest close.
            # Formula: ((current price - previous close) / previous close) x 100.
            # This helps users quickly see whether the ticker moved up or down.
            market_rows.append({
                # This adds the successful market data for the ticker into the market_rows list.
                "ticker": ticker,
                # This stores the ticker symbol so it can be displayed in the dashboard table.
                "current_price": round(current_price, 2),
                # This stores the current price rounded to 2 decimal places for cleaner display.
                "last_price": round(current_price, 2),
                # This stores the last available price.
                # In this version, last_price and current_price are the same because the data comes from the latest closing price.
                "previous_trading_day_close": round(previous_close, 2),
                # This stores the previous trading day's close rounded to 2 decimal places.
                "change_percent": round(change_percent, 2),
                # This stores the percentage change rounded to 2 decimal places.
            })
        except Exception as error:
            # This catches any error that happens while getting or processing data for a ticker.
            # It prevents one broken ticker from crashing the whole Django dashboard page.
            print(f"Yahoo Finance error for {ticker}: {error}")
            # This prints the error in the VS Code terminal.
            # This is useful for debugging because I can see which ticker failed and why.
            market_rows.append({
                # This adds a fallback row when an error happens.
                "ticker": ticker,
                # This still shows the ticker name in the dashboard table.
                "current_price": "Unavailable",
                # This tells the user that the current price could not be loaded.
                "last_price": "Unavailable",
                # This tells the user that the last price could not be loaded.
                "previous_trading_day_close": "Unavailable",
                # This tells the user that the previous close could not be loaded.
                "change_percent": "Unavailable",
                # This tells the user that the percentage change could not be calculated.
            })
    cache.set(cache_key, market_rows, 300)
    # This saves the completed market_rows list into Django's cache.
    # The number 300 means the data is cached for 300 seconds, which is 5 minutes.
    # This helps performance because the dashboard does not call Yahoo Finance on every single page refresh.
    return market_rows
    # This returns the final list of market data rows.
    # The dashboard view sends this list to the template, and the template displays it in the Latest Market Snapshot table.