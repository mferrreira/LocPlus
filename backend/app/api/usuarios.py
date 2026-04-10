from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.models.usuarios import Usuario, ObjetivoConta
from app.models.clientes import Cliente
from app.models.empresas import Empresa
from app.models.saas_core import Plano, Assinatura
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários e Autenticação"])

@router.post("/cadastro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Trava de Segurança: O E-mail já existe?
    db_email = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Este e-mail já está em uso.")

    # 2. Trava de Segurança: O Documento (CPF/CNPJ) já existe?
    db_documento = db.query(Usuario).filter(Usuario.documento == usuario.documento).first()
    if db_documento:
        raise HTTPException(status_code=400, detail="Este CPF/CNPJ já está cadastrado.")

    # 3. Preparação do Tenant e Usuário
    if usuario.objetivo == ObjetivoConta.LOCADOR:
        nova_empresa = Empresa(nome_fantasia=usuario.nome_fantasia)
        db.add(nova_empresa)
        db.flush()
        
        # 3.1 Onboarding SaaS: O plano trial padrão
        plano_freemium = db.query(Plano).filter(Plano.nome == "Plano Freemium").first()
        if not plano_freemium:
            plano_freemium = Plano(nome="Plano Freemium", preco=0.0, max_maquinas=3, max_usuarios=1)
            db.add(plano_freemium)
            db.flush()
            
        nova_assinatura = Assinatura(
            empresa_id=nova_empresa.id,
            plano_id=plano_freemium.id,
            data_vencimento=datetime.utcnow() + timedelta(days=365)
        )
        db.add(nova_assinatura)
        
        novo_usuario = Usuario(
            email=usuario.email,
            senha_hash=get_password_hash(usuario.senha),
            objetivo=usuario.objetivo,
            tipo_entidade=usuario.tipo_entidade,
            nome_completo=usuario.nome_completo,
            documento=usuario.documento,
            telefone_celular=usuario.telefone_celular,
            telefone_fixo=usuario.telefone_fixo,
            rg=usuario.rg,
            data_nascimento=usuario.data_nascimento,
            viu_guia_cadastro=usuario.viu_guia_cadastro,
            empresa_id=nova_empresa.id,
            role="admin"
        )
        db.add(novo_usuario)
    else:
        novo_usuario = Usuario(
            email=usuario.email,
            senha_hash=get_password_hash(usuario.senha),
            objetivo=usuario.objetivo,
            tipo_entidade=usuario.tipo_entidade,
            nome_completo=usuario.nome_completo,
            documento=usuario.documento,
            telefone_celular=usuario.telefone_celular,
            telefone_fixo=usuario.telefone_fixo,
            rg=usuario.rg,
            data_nascimento=usuario.data_nascimento,
            viu_guia_cadastro=usuario.viu_guia_cadastro,
            empresa_id=None,
            role="locatario"
        )
        db.add(novo_usuario)
        db.flush()
        
        # Cliente (Locatário) global
        novo_perfil = Cliente(usuario_id=novo_usuario.id)
        db.add(novo_perfil)

    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.post("/login", status_code=status.HTTP_200_OK)
def login_usuario(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # O OAuth2PasswordRequestForm padrão usa 'username' por convenção, nós enviaremos o e-mail nele
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario or not verify_password(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    
    # Motor Real de JWT Multi-tenant
    from datetime import timedelta
    access_token = create_access_token(
        data={
            "sub": str(usuario.id),
            "tenant_id": usuario.empresa_id,
            "role": usuario.role
        }
    )
    
    refresh_token = create_refresh_token(
        data={
            "sub": str(usuario.id),
            "tenant_id": usuario.empresa_id,
            "role": usuario.role
        }
    )
    
    cliente_id = usuario.perfil_cliente[0].id if usuario.perfil_cliente else None

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "tipo_entidade": usuario.tipo_entidade,
        "objetivo": usuario.objetivo,
        "nome": usuario.nome_completo,
        "cliente_id": cliente_id
    }

class TokenRefresh(BaseModel):
    refresh_token: str

@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    import jwt
    import os
    SECRET_KEY = os.getenv("SECRET_KEY", "minha-chave-secreta-sasa-b2b")
    ALGORITHM = "HS256"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token_data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise credentials_exception
            
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    usuario = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if not usuario:
        raise credentials_exception
        
    new_access_token = create_access_token(
        data={
            "sub": str(usuario.id),
            "tenant_id": usuario.empresa_id,
            "role": usuario.role
        }
    )
    return {"access_token": new_access_token, "token_type": "bearer"}