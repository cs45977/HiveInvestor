from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from app.core.config import settings
from app.db.firestore import get_db

router = APIRouter()

@router.post("/users/login")
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_db)
):
    users_ref = db.collection("users")
    # Assuming username field in form is email
    query = users_ref.where("email", "==", form_data.username).limit(1).stream()
    user_doc = next((doc for doc in query), None)
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_data = user_doc.to_dict()
    if not security.verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user_data["id"], expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
