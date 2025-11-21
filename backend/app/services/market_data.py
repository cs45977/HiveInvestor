import httpx
from app.core.config import settings
from app.models.market import StockQuote
from fastapi import HTTPException, status

async def get_real_time_quote(symbol: str) -> StockQuote:
    url = "https://finnhub.io/api/v1/quote"
    params = {
        "symbol": symbol,
        "token": settings.FINNHUB_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Market data service unavailable"
        )
        
    data = response.json()
    
    # Finnhub returns c=0 if symbol is invalid (sometimes), or checks response
    if data.get("c") == 0 and data.get("pc") == 0:
         # Simple check for invalid symbol as Finnhub often returns 200 OK with 0s
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol {symbol} not found"
        )

    return StockQuote(
        symbol=symbol,
        price=data.get("c", 0.0),
        change=data.get("d", 0.0),
        percent_change=data.get("dp", 0.0)
    )
