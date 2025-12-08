import bcrypt
from app.utils.validators import is_strong_password

class PasswordManager:

    @staticmethod
    def hash_password(password: str)-> str:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hash_password: str)->bool:
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hash_password.encode('utf-8')
            )
        except Exception:
            return False

    @staticmethod
    def validate_strength(password:str)-> tuple[bool, str]:
        return is_strong_password(password=password)