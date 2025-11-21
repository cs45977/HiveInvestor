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
