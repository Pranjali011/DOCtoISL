from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token, verify_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


#SIGNUP
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username.strip(),
        email=user.email.lower(),
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Creates token after signup
    access_token = create_access_token({"sub": new_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }



#LOGIN
@router.post("/login")
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):

    # Checks if user exists
    user_db = db.query(User).filter(User.email == credentials.email.lower()).first()

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Verify password
    if not verify_password(credentials.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    # Creates JWT token
    access_token = create_access_token({"sub": user_db.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_db.id,
            "username": user_db.username,
            "email": user_db.email
        }
    }


#GET LOGGED-IN  as USER 
@router.get("/me", response_model=UserResponse)
def get_current_user(token: str, db: Session = Depends(get_db)):
    """
    Fetch user data from JWT token.
    Example frontend call: /auth/me?token=JWT_TOKEN
    """

    try:
        payload = verify_access_token(token)
        email: str = payload.get("sub")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_db = db.query(User).filter(User.email == email).first()

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user_db
