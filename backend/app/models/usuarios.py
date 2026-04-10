from sqlalchemy import Column, Integer, String, Boolean, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
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
    telefone_celular = Column(String, nullable=True)
    telefone_fixo = Column(String, nullable=True)
    
    # Campos Específicos PF
    rg = Column(String, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    
    # Controle de Sistema e Segurança
    is_ativo = Column(Boolean, default=True)
    is_verificado = Column(Boolean, default=False) # Para validação de E-mail/WhatsApp no futuro
    is_2fa_enabled = Column(Boolean, default=False)
    aceitou_termos_uso = Column(Boolean, default=False)
    
    # A Flag de UX que discutimos para o Product Tour
    viu_guia_cadastro = Column(Boolean, default=False)

    # SaaS Roles e Hierarquia de Tenant
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True) # Nullable porque Clientes(Locatários) não pertencem a um Tenant específico
    role = Column(String, default="admin") # "admin", "operador" -> Poderíamos usar Enum depois

    # V2 Relacionamentos
    empresa = relationship("Empresa", back_populates="usuarios")
    enderecos = relationship("Endereco", back_populates="usuario", cascade="all, delete-orphan")
    documentos_kyc = relationship("DocumentoKYC", back_populates="usuario", cascade="all, delete-orphan")
    representacoes = relationship("RepresentacaoB2B", foreign_keys="RepresentacaoB2B.representante_usuario_id", back_populates="representante", cascade="all, delete-orphan")