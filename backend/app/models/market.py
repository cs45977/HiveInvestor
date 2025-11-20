from pydantic import BaseModel

class StockQuote(BaseModel):
    symbol: str
    price: float
    change: float
    percent_change: float
