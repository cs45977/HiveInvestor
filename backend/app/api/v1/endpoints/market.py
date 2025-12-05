from fastapi import APIRouter, Depends, HTTPException, status
from app.api import deps
from app.services.market_data import get_real_time_quote
from app.models.market import StockQuote

router = APIRouter()

@router.get("/quote/{symbol}", response_model=StockQuote)
async def get_quote(
    symbol: str,
    current_user: dict = Depends(deps.get_current_user)
):
    quote = await get_real_time_quote(symbol)
    return quote

@router.get("/history/{symbol}")
async def get_history(
    symbol: str,
    resolution: str = 'D',
    limit: int = 100,
    current_user: dict = Depends(deps.get_current_user)
):
    from app.services.market_data import get_market_history
    return await get_market_history(symbol, resolution, limit)
