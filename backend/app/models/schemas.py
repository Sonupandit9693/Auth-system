from pydantic import BaseModel, Emailstr, Field
from typing import Optional, Dict


#request model
class RegisterRequset(BaseModel):
    email: Emailstr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=12)

class LoginRequset(BaseModel):
    email_or_username: str
    password: str

class RefreshTokenRequset(BaseModel):
    refresh_token: str


#response model
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int

class MessageReposne(BaseModel):
    message:str
    user_id:Optional[str]= None

class UsetResponse(BaseModel):
    user_id: str
    email: str
    username: str
    is_verified: bool

class ErrorResponse(BaseModel):
    detail: str