from fastapi import APIRouter, Depends
from typing import List
from app.api import deps
from app.models.trade import TradeResponse
from google.cloud import firestore

router = APIRouter()

@router.get("/", response_model=List[TradeResponse])
def get_transactions(
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    user_id = current_user["id"]
    # Note: 'where' and 'order_by' requires composite index in Firestore if strictly enforced, 
    # but simple queries usually work. 
    # However, order_by timestamp might require index if inequality filter used. 
    # Here we only use equality filter on user_id. It should be fine.
    
    query = db.collection("transactions").where("user_id", "==", user_id)
    # Depending on firestore client, we might need to handle ordering carefully or handle in client.
    # Let's try ordering.
    query = query.order_by("timestamp", direction=firestore.Query.DESCENDING)
    
    docs = query.stream()
    
    return [doc.to_dict() for doc in docs]
