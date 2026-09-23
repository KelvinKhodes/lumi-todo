import jwt
from datetime import datetime, timedelta, timezone
from app.schemas.authentication_dto import UserTokenDTO
from app.models.user import User

class JwtUtils:
    def __init__(self, secret: str):
        self._SECRET_KEY = secret

    def get_token(self, user: User) -> UserTokenDTO:
        return UserTokenDTO(access_token=self.create_access_token(user), refresh_token=self.create_refresh_token(user))

    def verify(self, token: str) -> dict:
        return jwt.decode(token, key=self._SECRET_KEY, algorithms="HS256")

    def create_access_token(self, user: User) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "iat": now,
            "exp": now + timedelta(hours=1),
        }
    
        return jwt.encode(payload, key=self._SECRET_KEY, algorithm="HS256")

    def create_refresh_token(self, user: User) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "iat": now,
            "exp": now + timedelta(days=7),
        }
    
        return jwt.encode(payload, key=self._SECRET_KEY, algorithm="HS256")