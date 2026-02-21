from app.infra.config.settings import settings
from app.infra.auth.jwt_service import JwtService
from app.infra.auth.password_hasher_bcrypt import BcryptPasswordHasher

token_service = JwtService(
    secret_key=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,
    access_minutes=settings.JWT_ACCESS_MINUTES,
)

password_hasher = BcryptPasswordHasher()