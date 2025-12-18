import pandas as pd
from typing import Dict, Any

def read_price_data(symbol: str, timeframe: str) -> Dict[str, Any]:
    """
    Fetch price data for a given symbol and timeframe.
    
    Args:
        symbol: Trading symbol (e.g., 'RELIANCE', 'INFY')
        timeframe: Timeframe for data (e.g., '1d', '1h', '5m')
    
    Returns:
        Dictionary containing price data
    """

    try:
        filepath = f"data/PriceData_26Nov.csv"
        df = pd.read_csv(filepath, parse_dates = ["Date"])

        # Standardizing columns
        df.columns = [c.lower() for c in df.columns]

        df = df[df["symbol"] == symbol]

        df = df[df["date"] >= "2006-01-01"].sort_values("date", ascending=True).tail(22*6)

        records = df.to_dict(orient="list")

        return {"ohlcv_data" : records}

    except Exception as e:
        return {"error": f"Failed to load data: {str(e)}"}