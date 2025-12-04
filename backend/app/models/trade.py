from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Literal, Optional
from enum import Enum

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class TimeInForce(str, Enum):
    DAY = "DAY"
    GTC = "GTC"

class TradeRequest(BaseModel):
    symbol: str
    quantity: int = Field(..., gt=0)
    type: Literal["BUY", "SELL"]
    order_type: OrderType = OrderType.MARKET
    limit_price: Optional[float] = None
    time_in_force: TimeInForce = TimeInForce.DAY

    @model_validator(mode='after')
    def validate_limit_price(self):
        if self.order_type == OrderType.LIMIT and self.limit_price is None:
            raise ValueError('Limit price is required for LIMIT orders')
        if self.limit_price is not None and self.limit_price <= 0:
            raise ValueError('Limit price must be greater than 0')
        return self

class TradeResponse(BaseModel):
    id: str
    user_id: str
    symbol: str
    type: str
    order_type: OrderType = OrderType.MARKET
    limit_price: Optional[float] = None
    time_in_force: TimeInForce = TimeInForce.DAY
    status: str = "EXECUTED" # PENDING, EXECUTED, CANCELLED
    quantity: int
    price_per_share: Optional[float] = None
    total_amount: Optional[float] = None
    commission: Optional[float] = None
    timestamp: datetime
