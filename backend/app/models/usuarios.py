from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String, nullable=False)
    cnpj = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String)
    
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, nullable=False)
    documento = Column(String, unique=True, index=True, nullable=False) 
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String)
    
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)