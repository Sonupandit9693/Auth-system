import jwt
import secrets
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict
from app.config import settings

class TokenManager:
    """
    Handels Token creation and validation
    """

    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.acccess_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refersh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    def create_access_token(self, user_id:str, email:str, username:str) -> str:
        payload = {
            "user_id": user_id,
            "email" : email,
            "username" : username,
            "type": "access",
            "exp": datetime.utcnow() + self.acccess_token_expires,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(32)
        }

        return jwt.encode(payload, self.secret_key, self.algorithm)

    def create_refresh_token(self) -> tuple[str, str]:
        token = secrets.token_urlsafe(64)
        token_hash = bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()
        return token, token_hash

    def verify_token(self, token:str, token_type:str="access") -> Optional[Dict]:
        try:
            payload = jwt.ecode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            if payload.get("type") != token_type:
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def verify_refersh_token(token:str, token_hash:str) -> bool:
        try:
            bcrypt.checkpw(token.encode(), token_hash.encode())
        except Exception:
            return False

token_manager = TokenManager() #TODO: global token manager instance