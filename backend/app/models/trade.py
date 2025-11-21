from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class TradeRequest(BaseModel):
    symbol: str
    quantity: int = Field(..., gt=0)
    type: Literal["BUY", "SELL"]

class TradeResponse(BaseModel):
    id: str
    user_id: str
    symbol: str
    type: str
    quantity: int
    price_per_share: float
    total_amount: float
    commission: float
    timestamp: datetime
