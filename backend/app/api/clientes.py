from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.clientes import Cliente
from app.schemas.clientes import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes (Locatários)"])

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    cliente_existente = db.query(Cliente).filter(Cliente.documento == cliente.documento).first()
    if cliente_existente:
        raise HTTPException(status_code=400, detail="Este Documento já está cadastrado.")

    novo_cliente = Cliente(nome=cliente.nome, documento=cliente.documento)
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente