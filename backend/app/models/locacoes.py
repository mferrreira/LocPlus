from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, DateTime, String, Boolean
from datetime import datetime
import enum
from app.core.database import Base

# 1. O ciclo de vida exato de um aluguel
class StatusLocacao(str, enum.Enum):
    ORCAMENTO = "orcamento"
    AGUARDANDO_ENTREGA = "aguardando_entrega"
    EM_ANDAMENTO = "em_andamento" # A máquina está na obra
    CONTESTACAO = "contestacao"   # Cliente abriu divergência nas primeiras 12h
    MAQUINA_PARADA = "maquina_parada" # Diárias congeladas (manutenção)
    FINALIZADO = "finalizado"     # A máquina voltou
    CANCELADO = "cancelado"

# 2. Desenhando a Tabela de Contratos
class Locacao(Base):
    __tablename__ = "locacoes"

    id = Column(Integer, primary_key=True, index=True)
    
    # A Santíssima Trindade (Chaves Estrangeiras)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    equipamento_id = Column(Integer, ForeignKey("equipamentos.id"), nullable=False)

    # Controle de Tempo
    data_inicio = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_fim_prevista = Column(DateTime, nullable=False)
    data_aceite_locatario = Column(DateTime, nullable=True) # O momento do Check-in do Cliente
    data_devolucao_real = Column(DateTime, nullable=True) # Preenchido só no fim do contrato

    # Financeiro e Logística
    valor_total = Column(Float, nullable=False)
    endereco_entrega = Column(String, nullable=True) # Para Canteiros de Obras específicos
    
    # Status da Operação
    status = Column(Enum(StatusLocacao), default=StatusLocacao.ORCAMENTO)
    
    # Preparando o terreno para as funções avançadas
    aluguel_representacao = Column(Boolean, default=False) 
    assinatura_digital_url = Column(String, nullable=True) # Para o futuro fluxo de vistoria