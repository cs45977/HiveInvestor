from fastapi import APIRouter, Depends, HTTPException, status
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
    query = db.collection("transactions").where("user_id", "==", user_id)
    query = query.order_by("timestamp", direction=firestore.Query.DESCENDING)
    docs = query.stream()
    return [doc.to_dict() for doc in docs]

@router.post("/{transaction_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_transaction(
    transaction_id: str,
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    doc_ref = db.collection("transactions").document(transaction_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    data = doc.to_dict()
    
    if data["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this transaction")
        
    if data["status"] != "PENDING":
        raise HTTPException(status_code=400, detail="Only PENDING transactions can be cancelled")
    
    doc_ref.update({"status": "CANCELLED"})
    return {"message": "Transaction cancelled successfully"}
