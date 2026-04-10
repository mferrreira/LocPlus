from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

# 1. Categorias Universais (Serve para Obras, Eventos, Hospitalar, etc.)
class CategoriaEquipamento(str, enum.Enum):
    LINHA_PESADA = "linha_pesada" # Ex: Tratores, Munck (Geralmente unitário e com manutenção cara)
    LINHA_LEVE = "linha_leve"     # Ex: Andaimes, Betoneiras pequenas
    VEICULOS = "veiculos"         # Ex: Caminhonetes, Caminhões
    MENSALISTAS = "mensalistas"   # Ex: Containers, Banheiros Químicos
    DIVERSOS = "diversos"         # Ex: Ferramentas pequenas, Mesas, Tendas



# 3. Desenhando a Tabela Universal de Estoque
class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String)
    
    # Se for uma frota de 50 cadeiras iguais, não tem número de série único.
    # Por isso, tiramos o "nullable=False" que ia quebrar o sistema de itens simples.
    numero_serie_patrimonio = Column(String, unique=True, index=True, nullable=True) 
    
    # Dados Técnicos (Passo 4.1)
    marca = Column(String, nullable=True)
    modelo = Column(String, nullable=True)
    ano_fabricacao = Column(Integer, nullable=True)
    
    # O coração financeiro Modular (Passo 4.4)
    valor_diaria = Column(Float, nullable=False)
    valor_semana = Column(Float, nullable=True)
    valor_quinzena = Column(Float, nullable=True)
    valor_mes = Column(Float, nullable=True)
    
    # URLs do MinIO (Passo 4.3)
    foto_visao_geral = Column(String, nullable=True)
    foto_painel = Column(String, nullable=True)
    foto_motor = Column(String, nullable=True)
    
    # A inteligência universal
    categoria = Column(Enum(CategoriaEquipamento), default=CategoriaEquipamento.DIVERSOS)
    
    # Gestão de Estoque Inteligente
    # Se for item único (Trator X), a quantidade é 1. Se for Andaime, pode ser 100.
    quantidade_total = Column(Integer, default=1) 
    quantidade_disponivel = Column(Integer, default=1)
    
    # Controle de Manutenção Automático (Ativado para Linha Pesada)
    em_manutencao = Column(Boolean, default=False)

    # Chave Estrangeira: A qual Locadora este equipamento pertence?
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    
    # O Pydantic só consegue fazer JoinedLoad porque instruimos o SQLAlchemy aqui!
    empresa = relationship("Empresa", backref="equipamentos")