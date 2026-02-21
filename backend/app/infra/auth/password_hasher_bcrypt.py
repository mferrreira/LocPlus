from passlib.context import CryptContext
from app.domain.ports.password_hasher import PasswordHasherPort

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BcryptPasswordHasher(PasswordHasherPort):
    def verify(self, plain_password: str, password_hash: str) -> bool:
        return _pwd.verify(plain_password, password_hash)
    
    def hash(self, plain_password: str) -> str:
        return _pwd.hash(plain_password)