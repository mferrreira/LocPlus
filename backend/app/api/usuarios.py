from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.usuarios import Usuario
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

    # 3. Preparação do Usuário (A Mágica da Criptografia acontece aqui)
    novo_usuario = Usuario(
        email=usuario.email,
        senha_hash=get_password_hash(usuario.senha), # A senha original morre aqui, só o hash vai pro banco
        objetivo=usuario.objetivo,
        tipo_entidade=usuario.tipo_entidade,
        nome_completo=usuario.nome_completo,
        documento=usuario.documento,
        telefone=usuario.telefone,
        viu_guia_cadastro=usuario.viu_guia_cadastro
    )

    # 4. Gravação no PostgreSQL
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario