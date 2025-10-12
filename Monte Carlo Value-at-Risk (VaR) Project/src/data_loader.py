
# src/data_loader.py
import yfinance as yf
import pandas as pd

def get_price_data(tickers, start="2022-01-01", end=None, auto_adjust=True):
    """
    Download price data robustly across yfinance versions.
    - If auto_adjust=True (default), adjusted prices are in 'Close'
    - If auto_adjust=False, adjusted prices are in 'Adj Close'
    Returns a DataFrame of prices (one column per ticker).
    """
    df = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=auto_adjust,   # key change
        progress=False,
        group_by="column"          # makes top-level fields: 'Close', 'Adj Close', etc.
    )

    # Pick the right field
    if isinstance(df.columns, pd.MultiIndex):
        # top level are fields
        fields = df.columns.get_level_values(0)
        if auto_adjust:
            field = "Close"
        else:
            field = "Adj Close" if "Adj Close" in fields else "Close"
        prices = df[field]
    else:
        # single-index columns (single ticker case)
        cols = df.columns
        if auto_adjust:
            field = "Close"
        else:
            field = "Adj Close" if "Adj Close" in cols else "Close"
        prices = df[[field]].copy()
        # rename to the ticker name
        name = tickers[0] if isinstance(tickers, (list, tuple)) else tickers
        prices.columns = [name]

    # Ensure Date index & sorted
    prices = prices.sort_index()
    return prices

def get_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Daily percentage returns."""
    return prices.pct_change().dropna()
