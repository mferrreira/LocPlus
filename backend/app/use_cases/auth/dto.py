from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class LoginInput:
    email: str
    password: str

@dataclass
class LoginOutput:
    access_token: str
    token_type: str
    user_id: UUID
    company_id: UUID
    role: str