from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuarios import Usuario
from app.models.enderecos import Endereco, TipoEndereco
from pydantic import BaseModel

router = APIRouter(prefix="/enderecos", tags=["Endereços e KYC"])

# O Schema do Endereço vive direto aqui pra acelerar a arquitetura sem sujar schemas.py
class EnderecoCreate(BaseModel):
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    tipo: TipoEndereco
    is_padrao: bool = False

class EnderecoResponse(EnderecoCreate):
    id: int
    class Config:
        from_attributes = True

@router.post("/", response_model=EnderecoResponse, status_code=status.HTTP_201_CREATED)
def adicionar_endereco(endereco: EnderecoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    novo_endereco = Endereco(
        usuario_id=current_user.id,
        cep=endereco.cep,
        logradouro=endereco.logradouro,
        numero=endereco.numero,
        complemento=endereco.complemento,
        bairro=endereco.bairro,
        cidade=endereco.cidade,
        estado=endereco.estado,
        tipo=endereco.tipo,
        is_padrao=endereco.is_padrao
    )
    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)
    return novo_endereco

@router.get("/", response_model=List[EnderecoResponse])
def listar_meus_enderecos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return db.query(Endereco).filter(Endereco.usuario_id == current_user.id).all()