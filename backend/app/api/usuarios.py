from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password
from app.models.usuarios import Usuario, ObjetivoConta
from app.models.clientes import Cliente
from app.models.empresas import Empresa
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
        telefone_celular=usuario.telefone_celular,
        telefone_fixo=usuario.telefone_fixo,
        rg=usuario.rg,
        data_nascimento=usuario.data_nascimento,
        razao_social=usuario.razao_social,
        nome_fantasia=usuario.nome_fantasia,
        inscricao_estadual=usuario.inscricao_estadual,
        viu_guia_cadastro=usuario.viu_guia_cadastro
    )

    # 4. Gravação Base
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # 5. Criar Perfil de Relacionamento (Gatilho automático)
    if novo_usuario.objetivo == ObjetivoConta.LOCADOR:
        novo_perfil = Empresa(usuario_id=novo_usuario.id)
        db.add(novo_perfil)
    else:
        novo_perfil = Cliente(usuario_id=novo_usuario.id)
        db.add(novo_perfil)
        
    db.commit()

    return novo_usuario


class UsuarioLogin(BaseModel):
    email: str
    senha: str

@router.post("/login", status_code=status.HTTP_200_OK)
def login_usuario(credenciais: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == credenciais.email).first()
    if not usuario or not verify_password(credenciais.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    
    # Como usamos localStorage na fundação inicial, o Token é um stub com a Role de interface
    return {
        "access_token": str(usuario.id),
        "tipo_entidade": usuario.tipo_entidade,
        "objetivo": usuario.objetivo,
        "nome": usuario.nome_completo
    }