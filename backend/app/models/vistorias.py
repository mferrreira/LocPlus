from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from datetime import datetime
import enum
from app.core.database import Base

# O sistema precisa saber se a foto é de quando a máquina saiu ou de quando voltou
class TipoVistoria(str, enum.Enum):
    ENTREGA = "entrega"
    DEVOLUCAO = "devolucao"

class Vistoria(Base):
    __tablename__ = "vistorias"

    id = Column(Integer, primary_key=True, index=True)
    
    # Hierarquia SaaS: A Locadora (Obrigatório para blindagem rápida de queries)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    # A Chave de Ouro: A qual contrato esta vistoria pertence?
    locacao_id = Column(Integer, ForeignKey("locacoes.id"), nullable=False)
    
    tipo = Column(Enum(TipoVistoria), nullable=False)
    data_vistoria = Column(DateTime, default=datetime.utcnow)
    
    # Métricas Quantitativas Obrigatórias (Passos do PRD)
    horimetro_odometro = Column(Float, nullable=True)
    nivel_combustivel = Column(String, nullable=True)
    
    # Checklist Físico Rápido (Booleans)
    check_pneus = Column(Boolean, default=True)
    check_vidros = Column(Boolean, default=True)
    check_lataria = Column(Boolean, default=True)
    check_painel = Column(Boolean, default=True)
    check_hidraulica = Column(Boolean, default=True)
    
    # Campo longo para o mecânico relatar arranhões, etc.
    observacoes = Column(String, nullable=True) 
    
    # Os caminhos (URLs) onde os arquivos PDF ou JPG ficarão salvos no servidor
    assinatura_cliente_url = Column(String, nullable=True)
    fotos_url = Column(String, nullable=True) # Podemos salvar vários caminhos separados por vírgula