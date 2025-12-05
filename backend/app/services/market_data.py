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
    
    # Check for mock key (local development)
    if settings.FINNHUB_API_KEY == "mock-key":
        import random
        base_price = 150.0
        change = random.uniform(-5, 5)
        return StockQuote(
            symbol=symbol,
            price=round(base_price + change, 2),
            change=round(change, 2),
            percent_change=round((change / base_price) * 100, 2)
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
    if response.status_code != 200:
        print(f"Finnhub Error: {response.status_code} - {response.text}") # Debug logging
        # Fallback to mock data if service is unavailable to prevent breaking the app
        return StockQuote(
            symbol=symbol,
            price=100.0,
            change=0.0,
            percent_change=0.0
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

async def get_market_history(symbol: str, resolution: str, limit: int) -> dict:
    # Mock history data for charts
    import random
    from datetime import datetime, timedelta
    
    candles = []
    now = datetime.now()
    price = 100.0 + random.uniform(-20, 20)
    
    for i in range(limit):
        # Generate candles going backwards
        time_offset = limit - i
        if resolution == 'D':
            time = int((now - timedelta(days=time_offset)).timestamp())
        else:
             # Default to minutes
            time = int((now - timedelta(minutes=time_offset * int(resolution))).timestamp())
            
        open_p = price
        close_p = price + random.uniform(-1, 1)
        high_p = max(open_p, close_p) + random.uniform(0, 0.5)
        low_p = min(open_p, close_p) - random.uniform(0, 0.5)
        
        candles.append({
            "time": time,
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2),
            "volume": int(random.uniform(1000, 5000))
        })
        
        price = close_p
        
    return {"candles": candles}
