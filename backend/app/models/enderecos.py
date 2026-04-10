from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class TipoEndereco(str, enum.Enum):
    SEDE = "sede"
    GALPAO = "galpao"
    CANTEIRO_OBRAS = "canteiro_obras"
    RESIDENCIAL = "residencial"

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    cep = Column(String, nullable=False)
    logradouro = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    
    tipo = Column(Enum(TipoEndereco), default=TipoEndereco.SEDE)
    is_padrao = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="enderecos")