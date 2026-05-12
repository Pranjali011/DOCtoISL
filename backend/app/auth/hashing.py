from passlib.context import CryptContext

# Configuration of Passlib CryptContext
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# Hash Password
def hash_password(password: str) -> str:
    """
    Hash password with bcrypt.

    bcrypt has a max limit of 72 bytes, so input is truncated
    for safety before hashing.
    """
    password = password[:72] 
    return pwd_context.hash(password)


# Verify Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    """
    plain_password = plain_password[:72] 
    return pwd_context.verify(plain_password, hashed_password)
