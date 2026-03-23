from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Importamos as regras de status que criamos no modelo do banco
from app.models.locacoes import StatusLocacao

# ==========================================
# SCHEMAS PARA LOCAÇÕES (Contratos e Orçamentos)
# ==========================================

# 1. Atributos base que todo contrato/orçamento precisa ter
class LocacaoBase(BaseModel):
    empresa_id: int
    cliente_id: int
    equipamento_id: int
    
    # Datas e Valores
    data_fim_prevista: datetime
    valor_total: float
    
    # Logística e Funcionalidades Avançadas
    endereco_entrega: Optional[str] = None
    aluguel_representacao: bool = False
    
    # Todo contrato nasce como Orçamento por padrão
    status: StatusLocacao = StatusLocacao.ORCAMENTO

# 2. Dados exigidos no momento de CRIAR uma nova Locação
class LocacaoCreate(LocacaoBase):
    pass # A data_inicio já é gerada automaticamente pelo banco de dados

# 3. Dados que DEVOLVEMOS para o Front-end após salvar no banco
class LocacaoResponse(LocacaoBase):
    id: int
    data_inicio: datetime
    data_devolucao_real: Optional[datetime] = None
    assinatura_digital_url: Optional[str] = None

    # Configuração vital: Ensina o Pydantic a ler os dados do SQLAlchemy (ORM)
    model_config = ConfigDict(from_attributes=True)