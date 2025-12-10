from collections import defaultdict
from datetime import datetime, timedelta
from threading import Lock
from typing import Optional


class RateLimiter:
    #simple in-memory rate limiter
    
    def __init__(self, max_attempts:int=5, window_seconds:int=60):
        self.max_attempts = max_attempts
        self.window = window_seconds
        self.attempts = defaultdict(list)
        self.lock = Lock()

    def is_allowed(self, indentifier:str) -> tuple[bool, Optional[int]]:
        with self.lock:
            now = datetime.utcnow()

            #clean old attempts outside the window
            self.attempts[indentifier] = [
                ts for ts in self.attempts[indentifier]
                if now - ts < timedelta(seconds=self.window)
            ]
        
            if len(self.attempts[indentifier]) >= self.max_attempts:
                oldest = self.attempts[indentifier][0]
                wait_time = int(oldest + self.window - now).total_seconds()
                return False, max(wait_time, 1)
            
            self.attempts[indentifier].append(now)
            return True, None

    def reset(self, indentifier:str) :
        """
        reset attempts for indentifier
        """

        with self.lock:
            if indentifier in self.attempts:
                del self.attempts[indentifier]


rate_limiter = RateLimiter(max_attempts=5, window_seconds=60)
