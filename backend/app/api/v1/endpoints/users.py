from fastapi import APIRouter, HTTPException, Request, status, Depends
from app.models.user import UserCreate, UserResponse
from app.db.firestore import get_db
from app.api.deps import get_current_user
from app.core import security
from app.models.portfolio import PortfolioInDB
from app.core.limiter import limiter
from datetime import datetime, timezone
from google.cloud import firestore
import uuid

router = APIRouter()


@firestore.transactional
def _create_user_atomically(transaction, email_ref, user_ref, portfolio_ref, user_doc, portfolio_data):
    """
    Atomically reserve the email and create the user + portfolio in one
    Firestore transaction.

    The previous implementation did a plain `where("email", "==", ...).stream()`
    read, and only afterwards issued a separate `.set()` write — classic
    read-then-write race: two concurrent registrations for the same email can
    both pass the "does it exist" check before either write lands, so both
    succeed and you end up with two user documents sharing one email.

    Firestore transactions require all reads to happen before any writes, so
    the existence check on `email_ref` below must come first. `email_ref`
    lives in a dedicated `emails` index collection keyed by the (lowercased)
    email address — that key IS the uniqueness constraint. If two requests
    race for the same email, Firestore's transaction contention detection
    forces one of them to retry and see the just-committed reservation from
    the other, so exactly one succeeds.
    """
    email_snapshot = email_ref.get(transaction=transaction)
    if email_snapshot.exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    transaction.set(email_ref, {"user_id": user_doc["id"]})
    transaction.set(user_ref, user_doc)
    transaction.set(portfolio_ref, portfolio_data)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register_user(request: Request, user: UserCreate, db=Depends(get_db)):
    normalized_email = user.email.strip().lower()
    user_id = str(uuid.uuid4())

    hashed_password = security.get_password_hash(user.password)

    user_doc = {
        "id": user_id,
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password
    }

    new_portfolio = PortfolioInDB(
        user_id=user_id,
        cash_balance=100000.0,
        total_value=100000.0,
        holdings=[],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    email_ref = db.collection("emails").document(normalized_email)
    user_ref = db.collection("users").document(user_id)
    portfolio_ref = db.collection("portfolios").document(user_id)

    transaction = db.transaction()
    _create_user_atomically(
        transaction, email_ref, user_ref, portfolio_ref, user_doc, new_portfolio.model_dump()
    )

    return user_doc

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


