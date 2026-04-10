from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.storage import upload_file_to_minio
from app.models.usuarios import Usuario
from app.models.documentos_kyc import DocumentoKYC, TipoDocumento, StatusVerificacao
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/kyc", tags=["Confiança e KYC"])

class DocumentoKYCResponse(BaseModel):
    id: int
    tipo_documento: str
    minio_s3_url: str
    status: str
    data_envio: datetime

    class Config:
        from_attributes = True

@router.post("/upload", response_model=DocumentoKYCResponse, status_code=status.HTTP_201_CREATED)
def enviar_documento_kyc(
    tipo: TipoDocumento = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Envia pro bucket MinIO seguro
    nome_arquivo = f"kyc_user{current_user.id}_{tipo}_{file.filename}"
    s3_url = upload_file_to_minio(file, nome_arquivo)
    
    # Salva no Banco de Dados (Status: Pendente para Auditoria Administrativa)
    novo_doc = DocumentoKYC(
        usuario_id=current_user.id,
        tipo_documento=tipo,
        minio_s3_url=s3_url,
        status=StatusVerificacao.PENDENTE
    )
    db.add(novo_doc)
    db.commit()
    db.refresh(novo_doc)
    
    return novo_doc

@router.get("/", response_model=List[DocumentoKYCResponse])
def listar_meus_documentos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return db.query(DocumentoKYC).filter(DocumentoKYC.usuario_id == current_user.id).all()
