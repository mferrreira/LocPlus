from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class User:
    id: UUID
    company_id: UUID
    full_name: str
    role: str
    email: str
    password_hash: str
    is_active: bool

