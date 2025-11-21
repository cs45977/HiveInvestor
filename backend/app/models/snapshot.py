from pydantic import BaseModel
from datetime import datetime

class PortfolioSnapshot(BaseModel):
    user_id: str
    date: str # YYYY-MM-DD
    total_value: float
    timestamp: datetime
