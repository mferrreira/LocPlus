from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class StatusRepresentacao(str, enum.Enum):
    ATIVA = "ativa"
    PENDENTE = "pendente"
    REVOGADA = "revogada"

class RepresentacaoB2B(Base):
    __tablename__ = "representacoes_b2b"

    id = Column(Integer, primary_key=True, index=True)
    representante_usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    cnpj_cliente_final = Column(String, index=True, nullable=False)
    razao_social_cliente_final = Column(String, nullable=False)
    comprovante_autorizacao_url = Column(String, nullable=False)  # S3 URL
    status_aprovacao = Column(Enum(StatusRepresentacao), default=StatusRepresentacao.PENDENTE)

    representante = relationship("Usuario", foreign_keys=[representante_usuario_id], back_populates="representacoes")
