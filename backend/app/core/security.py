from passlib.context import CryptContext

# Configuramos o motor do Passlib para usar exclusivamente o algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Recebe a senha limpa (ex: senha123) e devolve um hash incompreensível."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha digitada no login com o hash salvo no banco de dados."""
    return pwd_context.verify(plain_password, hashed_password)