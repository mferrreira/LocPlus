from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    
    # Identidade Publica Marketplace
    nome_fantasia = Column(String, nullable=True) # Pode ser preenchido gradativamente
    avaliacao = Column(Float, default=5.0)
    
    # Empresa é o Root (Tenant), então ela possui usuários subordinados a ela
    usuarios = relationship("Usuario", back_populates="empresa", cascade="all, delete-orphan")