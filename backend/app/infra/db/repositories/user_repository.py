from app.domain.entities.user import User
from app.infra.db.models.user_model import UserModel
from app.domain.ports.user_repository import UserRepositoryPort
from app.infra.db.utils.to_entity import to_entity


class SqlAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, session): self.session = session

    def get_by_email(self, email: str) -> User | None:
        m = self.session.query(UserModel).filter(UserModel.email == email).one_or_none()
        return to_entity(m) if m else None