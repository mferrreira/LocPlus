from pydantic import BaseModel, ConfigDict
from typing import Optional

# ==========================================
# SCHEMAS PARA LOGÍSTICA (Múltiplos Endereços)
# ==========================================

class EnderecoBase(BaseModel):
    apelido: str
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    is_principal: bool = False
    
    # Opcionais, mas a rota exigirá que pelo menos um seja preenchido
    cliente_id: Optional[int] = None
    empresa_id: Optional[int] = None

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoResponse(EnderecoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)