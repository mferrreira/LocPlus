from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
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
    
    # A Chave de Ouro: A qual contrato esta vistoria pertence?
    locacao_id = Column(Integer, ForeignKey("locacoes.id"), nullable=False)
    
    tipo = Column(Enum(TipoVistoria), nullable=False)
    data_vistoria = Column(DateTime, default=datetime.utcnow)
    
    # Campo longo para o mecânico relatar arranhões, nível de combustível, etc.
    observacoes = Column(String, nullable=True) 
    
    # Os caminhos (URLs) onde os arquivos PDF ou JPG ficarão salvos no servidor
    assinatura_cliente_url = Column(String, nullable=True)
    fotos_url = Column(String, nullable=True) # Podemos salvar vários caminhos separados por vírgula