from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.vistorias import TipoVistoria

# ==========================================
# SCHEMAS PARA VISTORIAS E UPLOADS
# ==========================================

class VistoriaResponse(BaseModel):
    id: int
    locacao_id: int
    tipo: TipoVistoria
    data_vistoria: datetime
    observacoes: Optional[str] = None
    assinatura_cliente_url: Optional[str] = None
    fotos_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)