from pydantic import BaseModel, ConfigDict
from typing import Optional

# Importamos as regras rígidas que criamos no modelo do banco
from app.models.equipamentos import CategoriaEquipamento

# ==========================================
# SCHEMAS PARA EQUIPAMENTOS (Estoque Universal)
# ==========================================

# 1. Atributos base que todo equipamento tem, independente do tamanho
class EquipamentoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    numero_serie_patrimonio: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano_fabricacao: Optional[int] = None
    
    valor_diaria: float
    valor_semana: Optional[float] = None
    valor_quinzena: Optional[float] = None
    valor_mes: Optional[float] = None
    
    foto_visao_geral: Optional[str] = None
    foto_painel: Optional[str] = None
    foto_motor: Optional[str] = None
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