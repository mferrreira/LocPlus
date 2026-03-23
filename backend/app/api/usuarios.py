

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importações da nossa própria arquitetura
from app.core.database import get_db
from app.models.usuarios import Empresa
from app.schemas.usuarios import EmpresaCreate, EmpresaResponse

# Cria o "Roteador" (Um mini-FastAPI dedicado apenas a empresas)
router = APIRouter(prefix="/empresas", tags=["Empresas (Locadoras)"])

@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    
    # 1. Regra de Negócio: Impede cadastro de CNPJ duplicado
    empresa_existente = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()
    if empresa_existente:
        raise HTTPException(status_code=400, detail="Este CNPJ já está cadastrado no sistema.")

    # 2. Regra de Negócio: Impede cadastro de E-mail duplicado
    email_existente = db.query(Empresa).filter(Empresa.email == empresa.email).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="Este E-mail já está cadastrado no sistema.")

    # 3. Transforma o Schema (Pydantic) em um Modelo de Banco de Dados (SQLAlchemy)
    nova_empresa = Empresa(
        razao_social=empresa.razao_social,
        cnpj=empresa.cnpj,
        email=empresa.email,
        telefone=empresa.telefone
    )

    # 4. Executa a gravação física no PostgreSQL
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa) # Atualiza a variável para pegar o ID que o banco gerou

    # 5. Retorna os dados com sucesso para o Front-end
    return nova_empresa
    # ==========================================
# ROTA: LISTAR TODAS AS EMPRESAS
# ==========================================
@router.get("/", response_model=List[EmpresaResponse])
def listar_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    # 1. Vai até o banco de dados e busca as empresas
    # Usamos skip e limit como boa prática Sênior para paginação (não travar o servidor se tivermos 10.000 empresas)
    empresas = db.query(Empresa).offset(skip).limit(limit).all()
    
    # 2. Devolve a lista pronta para o Front-end
    return empresas