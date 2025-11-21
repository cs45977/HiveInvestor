from fastapi import APIRouter, Depends, HTTPException, status
from app.api import deps
from app.models.portfolio import Portfolio, PortfolioCreate, PortfolioInDB
from datetime import datetime, timezone

router = APIRouter()

@router.post("/", response_model=Portfolio, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    user_id = current_user["id"]
    portfolio_ref = db.collection("portfolios").document(user_id)
    
    if portfolio_ref.get().exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio already exists for this user"
        )
        
    new_portfolio = PortfolioInDB(
        user_id=user_id,
        cash_balance=100000.0,
        total_value=100000.0,
        holdings=[],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    portfolio_ref.set(new_portfolio.model_dump())
    
    return new_portfolio

@router.get("/me", response_model=Portfolio)
def get_portfolio(
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    user_id = current_user["id"]
    portfolio_ref = db.collection("portfolios").document(user_id)
    portfolio_doc = portfolio_ref.get()
    
    if not portfolio_doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
        
    return portfolio_doc.to_dict()
