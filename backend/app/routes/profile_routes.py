from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/profile", tags=["User Profile"])

# Pydantic Model
class UpdateProfileRequest(BaseModel):
    name: str | None = None
    email: str | None = None


# USER PROFILE
@router.get("/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    return {
        "id": user.id,
        "name": user.username,
        "email": user.email,
        "created_at": user.created_at,
    }


# UPDATE USER PROFILE
@router.put("/{user_id}")
def update_profile(user_id: int, payload: UpdateProfileRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    if payload.name:
        user.username = payload.name
    if payload.email:
        user.email = payload.email

    db.commit()
    db.refresh(user)

    return {"message": "Profile updated", "user": {
        "id": user.id,
        "name": user.username,
        "email": user.email
    }}
