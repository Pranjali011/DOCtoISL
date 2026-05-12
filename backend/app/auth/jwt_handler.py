from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import settings

ALGORITHM = "HS256"


# Create JWT Access Token
def create_access_token(data: dict) -> str:
    """
    Create a signed JWT token.
    
    data must contain "sub" field (subject = user email or ID)
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),  # Issued at
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# Verify & Decode JWT Token
def verify_access_token(token: str) -> dict:
    """
    Decode and verify JWT token.
    Returns the token payload if valid.
    Raises JWTError if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise JWTError("Invalid or expired token")
