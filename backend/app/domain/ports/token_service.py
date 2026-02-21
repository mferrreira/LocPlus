from typing import Protocol
from uuid import UUID

class TokenServicePort(Protocol):
    def create_access_token(self, *, user_id: UUID, company_id: UUID, role: str) -> str:
        ...
    
    def decode_access_token(self, token: str) -> dict:
        ...