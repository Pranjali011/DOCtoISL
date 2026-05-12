from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


#   BASE USER SCHEMA (Shared Fields)
class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


#   USER CREATE (Signup)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)  # bcrypt limit


#   USER LOGIN
class UserLogin(BaseModel):
    email: EmailStr
    password: str


#   RESPONSE MODEL
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True   
