from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app.services.evaluation import update_all_portfolios_total_value, generate_leaderboards
from app.models.leaderboard import Leaderboard
from typing import List

router = APIRouter()

@router.post("/admin/evaluate", status_code=200)
async def trigger_evaluation(
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    # In real app, check for admin role here
    await update_all_portfolios_total_value(db)
    await generate_leaderboards(db)
    return {"message": "Evaluation triggered successfully"}

@router.get("/{window}", response_model=Leaderboard)
def get_leaderboard(
    window: str,
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    if window not in ["1d", "7d", "30d", "90d"]:
        raise HTTPException(status_code=400, detail="Invalid window")
        
    doc = db.collection("leaderboards").document(window).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Leaderboard not found")
        
    return doc.to_dict()
