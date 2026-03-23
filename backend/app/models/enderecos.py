from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.core.database import Base

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamentos Múltiplos
    # Um endereço pode pertencer a um Cliente (Locatário) ou a uma Empresa (Matriz Locadora)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True)

    # Identificação do Local
    apelido = Column(String, nullable=False) # Ex: "Obra Zona Sul", "Sede Matriz"
    
    # Dados Logísticos para Cálculo de Frete
    cep = Column(String, nullable=False)
    logradouro = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)

    # Inteligência de Sistema
    is_principal = Column(Boolean, default=False) # Define qual é o endereço de faturamento padrão