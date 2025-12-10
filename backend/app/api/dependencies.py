from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict
from app.services.token_manager import token_manager

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials=Depends(security)
)->Dict:
    """
    dependncy to get authenticated user
    """

    token = credentials.credentials
    paylod = token_manager.verify_token(token, "access")
    if not paylod:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="nvalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return paylod