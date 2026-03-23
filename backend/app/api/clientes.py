from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importações da nossa arquitetura
from app.core.database import get_db
from app.models.usuarios import Cliente
from app.schemas.usuarios import ClienteCreate, ClienteResponse

# Roteador dedicado apenas aos Clientes
router = APIRouter(prefix="/clientes", tags=["Clientes (Locatários)"])

# ==========================================
# CADASTRAR NOVO CLIENTE (POST)
# ==========================================
@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    
    # Regra: Impede documento (CPF/CNPJ) duplicado
    cliente_existente = db.query(Cliente).filter(Cliente.documento == cliente.documento).first()
    if cliente_existente:
        raise HTTPException(status_code=400, detail="Este Documento já está cadastrado no sistema.")

    # Regra: Impede E-mail duplicado
    email_existente = db.query(Cliente).filter(Cliente.email == cliente.email).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="Este E-mail já está cadastrado no sistema.")

    # Prepara os dados para o PostgreSQL
    novo_cliente = Cliente(
        nome_completo=cliente.nome_completo,
        documento=cliente.documento,
        email=cliente.email,
        telefone=cliente.telefone
    )

    # Salva no banco e atualiza para pegar o ID gerado
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente

# ==========================================
# LISTAR CLIENTES (GET)
# ==========================================
@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Busca paginada para manter a API rápida e não sobrecarregar a memória
    clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return clientes