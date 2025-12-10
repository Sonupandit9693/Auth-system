from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict


#request model
class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=12)

class LoginRequest(BaseModel):
    email_or_username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str


#response model
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int

class MessageResponse(BaseModel):
    message:str
    user_id:Optional[str]= None

class UserResponse(BaseModel):
    user_id: str
    email: str
    username: str
    is_verified: bool

class ErrorResponse(BaseModel):
    detail: str