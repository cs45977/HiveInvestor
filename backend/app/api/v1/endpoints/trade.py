from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api import deps
from app.models.trade import TradeRequest, TradeResponse
from app.services import trading
from google.cloud import firestore

router = APIRouter()

@router.post("/", response_model=TradeResponse)
async def execute_trade_endpoint(
    trade_request: TradeRequest,
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    return await trading.execute_trade(current_user["id"], trade_request, db)

@router.get("/", response_model=List[TradeResponse])
def get_trade_history(
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    """
    Fetch trade history for the current user.
    """
    user_id = current_user["id"]
    transactions_ref = db.collection("transactions")
    
    # Query transactions for this user, ordered by timestamp descending
    query = transactions_ref.where("user_id", "==", user_id).order_by("timestamp", direction=firestore.Query.DESCENDING)
    
    docs = query.stream()
    history = []
    
    for doc in docs:
        data = doc.to_dict()
        # Ensure ID is included if it's not in the document body
        if "id" not in data:
            data["id"] = doc.id
        history.append(data)
        
    return history
