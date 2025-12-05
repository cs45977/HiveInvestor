from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserCreate, UserResponse
from app.db.firestore import get_db
from app.api.deps import get_current_user
from app.core import security
from app.models.portfolio import PortfolioInDB
from datetime import datetime, timezone
import uuid

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db=Depends(get_db)):
    users_ref = db.collection("users")
    
    # Check for duplicates
    # Note: This is not atomic, but sufficient for MVP/Simulated env. 
    # Ideally use a transaction or unique index constraints in DB.
    existing_users = list(users_ref.where("email", "==", user.email).stream())
    if existing_users:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())
    
    hashed_password = security.get_password_hash(user.password)
    
    user_doc = {
        "id": user_id,
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password
    }
    
    users_ref.document(user_id).set(user_doc)
    
    # Create default portfolio
    new_portfolio = PortfolioInDB(
        user_id=user_id,
        cash_balance=100000.0,
        total_value=100000.0,
        holdings=[],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.collection("portfolios").document(user_id).set(new_portfolio.model_dump())
    
    return user_doc

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

