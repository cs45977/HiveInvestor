from pydantic import BaseModel
from typing import List

class StockQuote(BaseModel):
    symbol: str
    price: float
    change: float
    percent_change: float
    
class Candle(BaseModel):
    time: int # Unix timestamp
    open: float
    high: float
    low: float
    close: float
    volume: int = 0

class HistoryResponse(BaseModel):
    symbol: str
    candles: List[Candle]
