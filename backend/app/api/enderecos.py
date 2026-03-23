from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enderecos import Endereco
from app.schemas.enderecos import EnderecoCreate, EnderecoResponse

router = APIRouter(prefix="/enderecos", tags=["Logística e Endereços"])

@router.post("/", response_model=EnderecoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_endereco(endereco: EnderecoCreate, db: Session = Depends(get_db)):
    
    # Trava Sênior: Um endereço não pode ficar "órfão" no banco
    if not endereco.cliente_id and not endereco.empresa_id:
        raise HTTPException(
            status_code=400, 
            detail="O endereço precisa estar vinculado a um Cliente (Locatário) ou Empresa (Locadora)."
        )

    novo_endereco = Endereco(**endereco.model_dump())
    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)

    return novo_endereco

@router.get("/", response_model=List[EnderecoResponse])
def listar_enderecos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Endereco).offset(skip).limit(limit).all()