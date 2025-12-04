from fastapi import APIRouter, Depends, HTTPException, status
from app.api import deps
from app.services.market_data import get_real_time_quote, get_historical_data
from app.models.market import StockQuote, HistoryResponse
from typing import Optional

router = APIRouter()

@router.get("/quote/{symbol}", response_model=StockQuote)
async def get_quote(
    symbol: str
):
    quote = await get_real_time_quote(symbol)
    return quote

@router.get("/history/{symbol}", response_model=HistoryResponse)
async def get_history(
    symbol: str,
    resolution: str = 'D',
    limit: int = 100
):
    return await get_historical_data(symbol, resolution, limit)
