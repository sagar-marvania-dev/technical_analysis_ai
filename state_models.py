from typing import List, Dict, Any, Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ShastraState(TypedDict):
    symbol : str | None 
    timeframe : str | None
    ohlcv_data : List[Dict[str, Any]] | None = None
    messages: Annotated[list[BaseMessage], add_messages]




