from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any

class ma_crossover_input(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ohlcv_data: Dict[str, Any] = Field(..., description="Dictionary containing price data. The dictionary must include: date and close.")
    fast_ma: int = Field(..., description="Window length for the fast moving average.", gt=0)
    slow_ma: int = Field(..., description="Window length for the slow moving average.", gt=0)

class price_crossover_input(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ohlcv_data: Dict[str, Any] = Field(..., description="Dictionary containing price data. The dictionary must include: date and close.")
    ma: int = Field(..., description="Window length for the moving average.", gt=0)
    

