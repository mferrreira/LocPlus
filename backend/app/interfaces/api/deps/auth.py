from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.infra.di.singletons import token_service
from app.infra.auth.jwt_service import InvalidToken

bearer = HTTPBearer()

class CurrentUser:
    def __init__(self, user_id: UUID, company_id: UUID, role: str):
        self.user_id = user_id
        self.company_id = company_id
        self.role = role
 
def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> CurrentUser:
    try:
        payload = token_service.decode_access_token(creds.credentials)
        return CurrentUser(
            user_id=UUID(payload["sub"]),
            company_id=UUID(payload["company_id"]),
            role=str(payload["role"]),
        )
    except (InvalidToken, KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")