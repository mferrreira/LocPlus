from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.empresas import Empresa
from app.schemas.empresas import EmpresaCreate, EmpresaResponse

router = APIRouter(prefix="/empresas", tags=["Empresas (Locadoras)"])

@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    empresa_existente = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()
    if empresa_existente:
        raise HTTPException(status_code=400, detail="Este CNPJ já está cadastrado.")

    nova_empresa = Empresa(razao_social=empresa.razao_social, cnpj=empresa.cnpj)
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa