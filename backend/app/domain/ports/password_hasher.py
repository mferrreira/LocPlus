from typing import Protocol

class PasswordHasherPort(Protocol):
    def verify(self, plain_password: str, password_hash: str) -> bool:
        ...
    def hash(self, plain_password: str) -> str:
        ...