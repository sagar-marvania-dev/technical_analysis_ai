from langchain.tools import tool
from langgraph.prebuilt import ToolNode
import pandas as pd
from typing import Dict, Any
from langchain_core.tools import StructuredTool
from indicator_model import (ma_crossover_input, price_crossover_input)

@tool("ma_crossover")
def ma_crossover(ohlcv_data: dict, fast_ma: int, slow_ma: int) -> Dict:
    """
    Compute a moving-average crossover signal using percent difference.

    This function takes OHLCV price data in dictionary form, converts it into a
    pandas DataFrame, and calculates two moving averages: a fast window and a 
    slow window. The function then computes the **percent difference**
    between the fast and slow moving averages:

        pct_diff = (fast_ma - slow_ma) / slow_ma

    This normalized spread is scale-independent and serves as a stable
    crossover indicator:

        - pct_diff > 0   → fast MA is above slow MA (bullish)
        - pct_diff < 0   → fast MA is below slow MA (bearish)
        - zero-crossings → crossover events

    Parameters
    ----------
    df : dict
        Dictionary containing price data. The dictionary must include:
            - "date": list of timestamps
            - "close": list of closing prices
    fast_ma : int
        Window length for the fast moving average.
    slow_ma : int
        Window length for the slow moving average.

    Returns
    -------
    dict
        A dictionary containing:
            {
                "ma_spread_pct": {
                    "date": [...],
                    "ma_spread_pct": [...]
                }
            }
        where `ma_spread_pct` is the percent difference between fast and slow MAs.

    Notes
    -----
    - Percent difference is preferred over raw delta or ratio since it is
      scale-independent and provides a consistent signal across assets with
      different price levels.
    - The returned vector can be used directly for crossover detection,
      trend-filtering, feature engineering, or position sizing.

    """

    ## Convert the dictionary data into pandas DataFrame.
    price_data = pd.DataFrame(ohlcv_data)

    ## Calculate rolling mean for fast and slow window.
    price_data["fast_ma"] = price_data["close"].rolling(window=fast_ma).mean()
    price_data["slow_ma"] = price_data["close"].rolling(window=slow_ma).mean()
    
    ## Calculate the spread between fast and slow window moving averages.
    price_data["ma_spread_pct"] = price_data["fast_ma"].div(price_data["slow_ma"]) - 1

    ## Convert dataframe columns into dictionary.
    records = price_data[["date", "ma_spread_pct"]].tail(22*3).to_dict(orient = "list")

    return  {"ma_spread_pct" : records}

@tool("price_crossover")
def price_crossover(ohlcv_data: dict, ma: int) -> Dict:
    """
    Compute a price crossover signal using percent difference.

    This function takes OHLCV price data in dictionary form, converts it into a
    pandas DataFrame, and calculates moving averages: a moving average window. 
    The function then computes the **percent difference**
    between the price and moving average:

        pct_diff = (close - ma) / ma

    This normalized spread is scale-independent and serves as a stable
    crossover indicator:

        - pct_diff > 0   → close is above MA (bullish)
        - pct_diff < 0   → close is below MA (bearish)
        - zero-crossings → crossover events

    Parameters
    ----------
    df : dict
        Dictionary containing price data. The dictionary must include:
            - "date": list of timestamps
            - "close": list of closing prices
    ma : int
        Window length for the moving average.

    Returns
    -------
    dict
        A dictionary containing:
            {
                "price_spread_pct": {
                    "date": [...],
                    "price_spread_pct": [...]
                }
            }
        where `price_spread_pct` is the percent difference between price and ma.

    Notes
    -----
    - Percent difference is preferred over raw delta or ratio since it is
      scale-independent and provides a consistent signal across assets with
      different price levels.
    - The returned vector can be used directly for crossover detection,
      trend-filtering, feature engineering, or position sizing.

    """

    ## Convert the dictionary data into pandas DataFrame.
    price_data = pd.DataFrame(ohlcv_data)

    ## Calculate rolling mean for fast and slow window.
    price_data["ma"] = price_data["close"].rolling(window=ma).mean()
    
    ## Calculate the spread between fast and slow window moving averages.
    price_data["price_spread_pct"] = price_data["close"].div(price_data["ma"]) - 1

    ## Convert dataframe columns into dictionary.
    records = price_data[["date", "price_spread_pct"]].tail(22*3).to_dict(orient = "list")

    return  {"price_spread_pct" : records}


# structured_ma_crossover_tool = StructuredTool.from_function(
#                                     func=ma_crossover,
#                                     args_schema=ma_crossover_input,
#                                     name = "ma_crossover",
#                                     description="Compute Two Moving Average (MA) crossover indicator."
#                                 )

# structured_price_crossover_tool = StructuredTool.from_function(
#                                     func=price_crossover,
#                                     args_schema=price_crossover_input,
#                                     name = "price_crossover",
#                                     description="Compute Price and a Moving Average (MA) crossover indicator."
#                                 )

# tool_kit = [structured_ma_crossover_tool, structured_price_crossover_tool]


tool_kit = [ma_crossover, price_crossover]

custom_tool_node = ToolNode(tool_kit)


