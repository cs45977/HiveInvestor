from pydantic import BaseModel, Field, ConfigDict

class StockQuote(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    symbol: str
    price: float
    change: float
    percent_change: float
    mock_quote: bool = Field(False, alias="mock-quote")
