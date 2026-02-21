from typing import Protocol
from uuid import UUID
from app.domain.entities.user import User

class UserRepositoryPort(Protocol):
    def get_by_email(self, email: str) -> User | None: 
        ...
        
    def get_by_id(self, id: UUID) -> User | None: 
        ...