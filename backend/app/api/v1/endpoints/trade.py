from fastapi import APIRouter, Depends, HTTPException, status
from app.api import deps
from app.models.trade import TradeRequest, TradeResponse
from app.services import trading

router = APIRouter()

@router.post("/", response_model=TradeResponse)
async def execute_trade_endpoint(
    trade_request: TradeRequest,
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    return await trading.execute_trade(current_user["id"], trade_request, db)
