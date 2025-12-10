from datetime import datetime, timedelta
from typing import Optional, Dict
from app.services.token_manager import TokenManager
from app.services.password_manager import PasswordManager
from app.utils.validators import is_valid_email, is_valid_username
import bcrypt


class AuthService:
    """
    core authentication service
    """

    LOCKOUT_THRESOLD = 5
    LOCKOUT_DURATION = timedelta(minutes=30)

    def __init__(self, db_connection, token_manager:TokenManager, password_manager:PasswordManager):
        self.db = db_connection
        self.token_manager = token_manager
        self.password_manager = password_manager

    
    def register_user(
        self,
        email:str,
        username:str,
        password:str,
        ip_address:str,
        user_agent:str
    )-> tuple[bool, str, Optional[str]]:
        #register new user

        #validate input
        if not is_valid_email(email=email):
            return False, "Invalid email format", None
        
        if not is_valid_username(username=username):
            return False , "Username must be 3-50 alphanumeric characters", None
        
        is_strong, msg = self.password_manager.validate_strength(password)
        if not is_strong:
            return False, msg, None
        
        cursor = self.db.cursor()

        #check if user exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s OR username = %s",
            (email.lower(), username.lower())
        )

        if cursor.fetchone():
            return False, "User Already exists", None
        
        #hash password
        password_hash = self.password_manager.hash_password(password)

        try:
            cursor.execute("""
                INSERT INTO users (email, username, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (email.lower(), username.lower(), password_hash))

            user_id = cursor.fetchone()['id']

            #audit log
            cursor.execute("""
                INSERT INTO audit_logs
                (user_id, action, ip_address, user_agent, status)
                VALUES (%s, 'register', %s, %s, 'sucess')
            """, (user_id, ip_address, user_agent))

            self.db.commit()
            return True, "Registration successful", str(user_id)
        except Exception as e:
            self.db.rollback()
            print(f"Registration error: {e}")
            return False, "regisration failed", None

    def login_user(
        self,
        email_or_username:str,
        password:str,
        ip_address:str,
        user_agent:str
    )-> tuple[bool, str, Optional[str]]:
        cursor = self.db.cursor()

        #find user
        cursor.execute("""
            SELECT id, email, username, password_hash, is_verified,
                is_active, failed_login_attempts, locked_until
            FROM users
            WHERE email = %s OR username = %s
        """, (email_or_username.lower(), email_or_username.lower()))

        user = cursor.fetchone()
        if not user:
            self._log_failed_login(None, ip_address, user_agent, "user_not_found")
            return False, "Invalid credentials", None
        
        user_id = user['id']
        locked_until = user['locked_until']
        failed_attempts = user['failed_login_attempts']

        #check if locked
        if locked_until and datetime.utcnow() < locked_until:
            remaining = int((locked_until - datetime.utcnow()).total_seconds() / 60)
            return False, f"Account locked. Try again in {remaining} minutes", None
        
        # check if active
        if not user['is_active']:
            return False, "Account is deactivated", None


        # verify password
        if not self.password_manager.verify_password(password, user['password_hash']):
            failed_attempts += 1
            
            if failed_attempts >= self.LOCKOUT_THRESHOLD:
                cursor.execute("""
                    UPDATE users
                    SET failed_login_attempts = %s, locked_until = %s
                    WHERE id = %s
                """, (failed_attempts, datetime.utcnow() + self.LOCKOUT_DURATION, user_id))
            else:
                cursor.execute("""
                    UPDATE users SET failed_login_attempts = %s WHERE id = %s
                """, (failed_attempts, user_id))
            
            self.db.commit()
            self._log_failed_login(user_id, ip_address, user_agent, "wrong_password")
            return False, "Invalid credentials", None
        
        #reset failed attempts
        cursor.execute("""
            UPDATE users
            SET failed_login_attempts = 0, locked_until = NULL
            WHERE id = %s
        """, (user_id,))
        
        #create tokens
        access_token = self.token_manager.create_access_token(
            str(user_id), user['email'], user['username']
        )
        
        refresh_token, refresh_token_hash = self.token_manager.create_refresh_token()
        
        #store session
        cursor.execute("""
            INSERT INTO sessions 
            (user_id, refresh_token_hash, device_info, expires_at)
            VALUES (%s, %s, %s, %s)
        """, (
            user_id,
            refresh_token_hash,
            f'{{"ip": "{ip_address}", "user_agent": "{user_agent}"}}',
            datetime.utcnow() + self.token_manager.refersh_token_expires
        ))

        #audit log
        cursor.execute("""
            INSERT INTO audit_logs 
            (user_id, action, ip_address, user_agent, status)
            VALUES (%s, 'login', %s, %s, 'success')
        """, (user_id, ip_address, user_agent))
        
        self.db.commit()
        
        return True, "Login successful", {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 900
        }

    def refresh_access_token(self, refresh_token: str) -> tuple[bool, str, Optional[str]]:
        """refresh access token"""
        
        cursor = self.db.cursor()
        
        #get all active sessions
        cursor.execute("""
            SELECT s.id, s.user_id, s.refresh_token_hash,
                u.email, u.username, u.is_active
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.expires_at > %s
        """, (datetime.utcnow(),))
        
        sessions = cursor.fetchall()
        
        #verify token
        valid_session = None
        for session in sessions:
            if self.token_manager.verify_refresh_token(refresh_token, session['refresh_token_hash']):
                valid_session = session
                break
        
        if not valid_session:
            return False, "Invalid refresh token", None
        
        if not valid_session['is_active']:
            return False, "Account deactivated", None
        
        #create new access token
        access_token = self.token_manager.create_access_token(
            str(valid_session['user_id']),
            valid_session['email'],
            valid_session['username']
        )
        
        #update session
        cursor.execute("""
            UPDATE sessions SET last_used_at = %s WHERE id = %s
        """, (datetime.utcnow(), valid_session['id']))
        
        self.db.commit()
        
        return True, "Token refreshed", access_token
    
    def logout_user(self, refresh_token: str) -> tuple[bool, str]:
        """Logout user"""
        cursor = self.db.cursor()
        
        #find and delete matching sessions
        cursor.execute("SELECT id, refresh_token_hash FROM sessions WHERE expires_at > %s", (datetime.utcnow(),))
        sessions = cursor.fetchall()
        
        for session in sessions:
            if self.token_manager.verify_refresh_token(refresh_token, session['refresh_token_hash']):
                cursor.execute("DELETE FROM sessions WHERE id = %s", (session['id'],))
                self.db.commit()
                return True, "Logged out successfully"
        
        return False, "Invalid token"
    

    def _log_failed_login(self, user_id, ip_address, user_agent, reason):
        #log failed login
        curr = self.db.cursor()
        curr.execute("""
            INSERT INTO audit_logs
            (user_id, action, ip_address, user_agent, status, metadata)
            VALUES (%s, 'login), %s, %s, 'failed', %s)
        """, (user_id, ip_address, user_agent, f'{{"reason": "{reason}"}}'))

        self.db.commit()
