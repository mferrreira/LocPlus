from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.core.database import Base

class TipoDocumento(str, enum.Enum):
    CNH = "cnh"
    RG = "rg"
    CONTRATO_SOCIAL = "contrato_social"
    COMPROVANTE_RESIDENCIA = "comprovante_residencia"

class StatusVerificacao(str, enum.Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"

class DocumentoKYC(Base):
    __tablename__ = "documentos_kyc"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    tipo_documento = Column(Enum(TipoDocumento), nullable=False)
    minio_s3_url = Column(String, nullable=False)
    status = Column(Enum(StatusVerificacao), default=StatusVerificacao.PENDENTE)
    data_envio = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="documentos_kyc")
