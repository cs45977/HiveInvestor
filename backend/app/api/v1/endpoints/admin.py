from fastapi import APIRouter, Depends, HTTPException, status
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.get("/config-status")
def get_config_status(
    current_user: dict = Depends(deps.get_current_user)
):
    """
    Checks the status of critical configurations.
    Only accessible by admins.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    is_finnhub_configured = settings.FINNHUB_API_KEY != "mock-key"
    
    return {
        "finnhub_configured": is_finnhub_configured,
        "finnhub_key_prefix": settings.FINNHUB_API_KEY[:4] if is_finnhub_configured else "mock"
    }
