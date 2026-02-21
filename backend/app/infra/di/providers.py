from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.db.session import get_db_session
from app.infra.db.user_repository_sqlalchemy import SqlAlchemyUserRepository
from app.infra.di.singletons import token_service, password_hasher
from app.use_cases.auth.login import LoginUseCase

def get_user_repo(db: Session = Depends(get_db_session)):
    return SqlAlchemyUserRepository(db)

def get_login_use_case(user_repo = Depends(get_user_repo)) -> LoginUseCase:
    return LoginUseCase(
        users=user_repo,
        hasher=password_hasher,
        tokens=token_service,
    )