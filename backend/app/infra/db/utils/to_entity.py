from app.domain.entities.user import User
from app.infra.db.models.user_model import UserModel

def to_entity(m: UserModel) -> User:
    return User(
        id=m.id,
        company_id=m.company_id,
        email=m.email,
        password_hash=m.password_hash,
        role=m.role,
        is_active=m.is_active,
    )
