from pydantic import BaseModel, ConfigDict
from typing import Optional

# Importamos as regras rígidas que criamos no modelo do banco
from app.models.equipamentos import CategoriaEquipamento, TipoCobranca

# ==========================================
# SCHEMAS PARA EQUIPAMENTOS (Estoque Universal)
# ==========================================

# 1. Atributos base que todo equipamento tem, independente do tamanho
class EquipamentoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    numero_serie_patrimonio: Optional[str] = None
    valor_base_locacao: float
    
    # Usamos os Enums para blindar as opções aceitas
    tipo_cobranca: TipoCobranca
    categoria: CategoriaEquipamento
    
    quantidade_total: int = 1
    
    # A Chave de Ouro: De qual locadora é este equipamento?
    empresa_id: int 

# 2. Dados exigidos no momento de CADASTRAR um equipamento
class EquipamentoCreate(EquipamentoBase):
    pass 

# 3. Dados que DEVOLVEMOS para o Front-end após salvar no banco
class EquipamentoResponse(EquipamentoBase):
    id: int
    quantidade_disponivel: int
    em_manutencao: bool

    # Configuração vital: Ensina o Pydantic a ler os dados do SQLAlchemy (ORM)
    model_config = ConfigDict(from_attributes=True)