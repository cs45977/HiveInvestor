import httpx
from app.core.config import settings
from app.models.market import StockQuote, Candle, HistoryResponse
from typing import List
import time
import random

async def get_historical_data(symbol: str, resolution: str, limit: int = 100) -> HistoryResponse:
    """
    resolution: '1', '5', '60', 'D', 'W', 'M'
    limit: number of data points
    """
    candles = []
    
    # Generate deterministic mock data based on symbol
    seed = sum(ord(c) for c in symbol)
    random.seed(seed)
    
    base_price = 150.0
    if symbol.upper() == "ES": base_price = 4000.0
    elif symbol.upper() == "NQ": base_price = 12000.0
    
    current_time = int(time.time())
    
    # Determine time step
    step = 86400 # D
    if resolution == '1': step = 60
    elif resolution == '5': step = 300
    elif resolution == '60': step = 3600
    elif resolution == 'W': step = 604800
    elif resolution == 'M': step = 2592000
    
    start_time = current_time - (limit * step)
    
    prev_close = base_price
    
    for i in range(limit):
        t = start_time + (i * step)
        
        # Random walk
        change_pct = (random.random() - 0.5) * 0.02 # 2% max swing
        
        open_p = prev_close
        close_p = open_p * (1 + change_pct)
        high_p = max(open_p, close_p) * (1 + random.random() * 0.01)
        low_p = min(open_p, close_p) * (1 - random.random() * 0.01)
        
        candles.append(Candle(
            time=t,
            open=round(open_p, 2),
            high=round(high_p, 2),
            low=round(low_p, 2),
            close=round(close_p, 2),
            volume=int(random.random() * 100000)
        ))
        prev_close = close_p
        
    return HistoryResponse(symbol=symbol, candles=candles)

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
        # Handle common typo APPL -> AAPL
        lookup_symbol = "AAPL" if symbol.upper() == "APPL" else symbol.upper()
        
        if lookup_symbol in ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA", "NFLX", "NVDA", "META"]: # Example recognized symbols
            base_price = sum(ord(c) for c in lookup_symbol) % 100 + 100 # Simple way to get a somewhat unique base price
            price = round(base_price + (random.random() - 0.5) * 10, 2) # +/- 5 change
            change = round((random.random() - 0.5) * 2, 2)
            percent_change = round((change / price) * 100, 2)
            
            return StockQuote(
                symbol=lookup_symbol,
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
