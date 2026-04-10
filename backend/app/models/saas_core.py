from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class StatusPgto(str, enum.Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    ATRASADO = "atrasado"

class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    preco = Column(Float, nullable=False)
    max_maquinas = Column(Integer, nullable=False)
    max_usuarios = Column(Integer, nullable=False)

    assinaturas = relationship("Assinatura", back_populates="plano")

class Assinatura(Base):
    __tablename__ = "assinaturas"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False, unique=True)
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=False)
    status_pagamento = Column(Enum(StatusPgto), default=StatusPgto.ATIVO)
    data_vencimento = Column(DateTime, nullable=False)

    empresa = relationship("Empresa", backref="assinatura")
    plano = relationship("Plano", back_populates="assinaturas")

class Notificacao(Base):
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    titulo = Column(String, nullable=False)
    mensagem = Column(String, nullable=False)
    lida = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
