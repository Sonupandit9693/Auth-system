from fastapi import APIRouter, HTTPException, status, Request, Depends
from typing import Dict
from app.models.schemas import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    MessageResponse,
    UserResponse
)
from app.api.dependencies import get_current_user
from app.database import get_db_connection
from app.services.auth_service import AuthService
from app.services.password_manager import PasswordManager
from app.services.token_manager import token_manager
from app.services.rate_limiter import rate_limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])

#initalize services
password_manager = PasswordManager()

def get_auth_service():
    with get_db_connection() as conn:
        return AuthService(conn, token_manager, password_manager)
    

def rate_limit(prefix: str):
    def dependency(req: Request):
        allowed, wait_time = rate_limiter.is_allowed(f"{prefix}_{req.client.host}")
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many attempts. Try again in {wait_time} seconds"
            )
    return dependency


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
    _: None = Depends(rate_limit("register"))
):
    success, message, user_id = auth_service.register_user(
        email=request.email,
        username=request.username,
        password=request.password,
        ip_address=None, user_agent=""
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    return MessageResponse(message=message, user_id=user_id)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
    _: None = Depends(rate_limit("login"))
):
    success, message, tokens = auth_service.login_user(
        email_or_username=request.email_or_username,
        password=request.password,
        ip_address=None, user_agent=""
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

    return TokenResponse(**tokens)


@router.post("/refresh")
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    success, message, access_token = auth_service.refresh_access_token(request.refresh_token)

    if not success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

    return {"access_token": access_token, "token_type": "Bearer", "expires_in": 900}


@router.post("/logout", response_model=MessageResponse)
async def logout(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    success, message = auth_service.logout_user(request.refresh_token)

    if not success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

    return MessageResponse(message=message)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    return UserResponse(**current_user, is_verified=True)


@router.get("/protected")
async def protected_route(current_user: Dict = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user['username']}! This is a protected route.",
        "user_id": current_user["user_id"]
    }
