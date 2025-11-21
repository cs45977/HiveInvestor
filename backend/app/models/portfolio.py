from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PortfolioBase(BaseModel):
    cash_balance: float = 100000.0
    total_value: float = 100000.0

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioInDB(PortfolioBase):
    user_id: str
    holdings: List[dict] = []
    created_at: datetime
    updated_at: datetime

class Portfolio(PortfolioInDB):
    pass
