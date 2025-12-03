import httpx
from app.core.config import settings
from app.models.market import StockQuote
from fastapi import HTTPException, status
import random

async def get_real_time_quote(symbol: str) -> StockQuote:
    if settings.FINNHUB_API_KEY == "mock-key":
        # --- Mock Market Data Logic ---
        # Fixed mock symbol for consistent testing
        if symbol.upper() == "MOCK":
            return StockQuote(
                symbol="MOCK",
                price=150.00,
                change=1.50,
                percent_change=1.01
            )
        
        # Slightly randomized mock data for other symbols
        if symbol.upper() in ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA", "NFLX"]: # Example recognized symbols
            base_price = sum(ord(c) for c in symbol) % 100 + 100 # Simple way to get a somewhat unique base price
            price = round(base_price + (random.random() - 0.5) * 10, 2) # +/- 5 change
            change = round((random.random() - 0.5) * 2, 2)
            percent_change = round((change / price) * 100, 2)
            
            return StockQuote(
                symbol=symbol.upper(),
                price=price,
                change=change,
                percent_change=percent_change
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mock symbol {symbol} not found in recognized list."
            )
        # --- End Mock Market Data Logic ---
    
    # Original Finnhub API Logic
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
            detail="Market data service unavailable or API key invalid"
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
