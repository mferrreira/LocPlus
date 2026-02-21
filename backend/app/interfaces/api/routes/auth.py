from fastapi import APIRouter, Depends, HTTPException, status

from app.interfaces.api.schemas.auth import LoginRequest, LoginResponse
from app.infra.di.providers import get_login_use_case
from app.use_cases.auth.login import LoginUseCase, InvalidCredentials
from app.use_cases.auth.dto import LoginInput

router = APIRouter("/api/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, use_case_handler: LoginUseCase = Depends(get_login_use_case)):
    try: 
        out = use_case_handler.execute(LoginInput(email=body.email, password=body.password))
        return LoginResponse(
            access_token=out.access_token,
            token_type=out.token_type,
            user_id=out.user_id,
            company_id=out.company_id,
            role=out.role
        )
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )