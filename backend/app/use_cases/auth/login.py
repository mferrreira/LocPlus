from app.domain.ports.token_service import TokenServicePort
from app.domain.ports.user_repository import UserReporitoryPort
from app.domain.ports.password_hasher import PasswordHasherPort
from app.use_cases.auth.dto import LoginInput, LoginOutput

class InvalidCredentials(Exception):
    pass

class LoginUseCase:

    def __init__(self, users: UserReporitoryPort, hasher: PasswordHasherPort, tokens: TokenServicePort):
        self.users = users
        self.hasher = hasher
        self.tokens = tokens

    def execute(self, input: LoginInput) -> LoginOutput:
        user = self.users.get_by_email(input.email.lower().strip())
        if not user or not user.is_active():
            raise InvalidCredentials()
    
        if not self.hasher.verify(input.password, user.password_hash):
            raise InvalidCredentials()
        
        access_token = self.tokens.create_access_token(user_id=user.id, company_id=user.company_id, role=user.role)

        return LoginOutput(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            company_id=user.company_id,
            role=user.role
        )