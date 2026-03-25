from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from app.core.database import Base

# Definindo as opções estritas de Onboarding
class TipoEntidade(str, enum.Enum):
    PF = "pessoa_fisica"
    PJ = "pessoa_juridica"

class ObjetivoConta(str, enum.Enum):
    LOCADOR = "disponibilizar_maquinas"
    LOCATARIO = "alugar_maquinas"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    
    # Credenciais de Acesso
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False) # NUNCA salvamos a senha real
    
    # Decisões do Onboarding
    objetivo = Column(Enum(ObjetivoConta), nullable=False)
    tipo_entidade = Column(Enum(TipoEntidade), nullable=False)
    
    # Dados Base (Comuns para PF e o Responsável da PJ)
    nome_completo = Column(String, nullable=False)
    documento = Column(String, unique=True, index=True, nullable=False) # CPF ou CNPJ
    telefone = Column(String, nullable=True)
    
    # Controle de Sistema e Segurança
    is_ativo = Column(Boolean, default=True)
    is_verificado = Column(Boolean, default=False) # Para validação de E-mail/WhatsApp no futuro
    
    # A Flag de UX que discutimos para o Product Tour
    viu_guia_cadastro = Column(Boolean, default=False)