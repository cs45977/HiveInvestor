from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api import deps
from app.models.user import UserResponse, UserRoleUpdate

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
def list_users(
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.require_admin)
):
    """Admin-only: list all registered users with their roles."""
    users_ref = db.collection("users")
    docs = users_ref.stream()
    return [doc.to_dict() for doc in docs]


@router.patch("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: str,
    role_update: UserRoleUpdate,
    db = Depends(deps.get_db),
    current_user: dict = Depends(deps.require_admin)
):
    """
    Admin-only: promote/demote a user's role.

    Guards against an admin locking themselves out by demoting their own
    last-admin account -- if this is the only admin in the system, demoting
    them to "user" would leave nobody able to manage roles going forward, so
    we block that specific case instead of allowing it silently.
    """
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    if role_update.role == "user" and user_id == current_user["id"]:
        users_ref = db.collection("users")
        admin_count = sum(
            1 for doc in users_ref.where("role", "==", "admin").stream()
        )
        if admin_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot demote the only remaining admin"
            )

    user_ref.update({"role": role_update.role})
    updated_doc = user_ref.get().to_dict()
    return updated_doc
