from datetime import datetime, timedelta, timezone
from uuid import UUID
from jose import jwt, JWTError
from app.domain.ports.token_service import TokenServicePort


class InvalidToken(Exception):
    pass

class JwtService(TokenServicePort):
    def __init__(self, *, secret_key: str, algorithm: str = "HS256", access_minutes: int = 60):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_minutes = access_minutes

    def create_access_token(self, *, user_id, company_id, role):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "company_id": str(company_id),
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self.access_minutes)).timestamp()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)


    def decode_access_token(self, token):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            raise InvalidToken() from e