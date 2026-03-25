from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.models.usuarios import TipoEntidade, ObjetivoConta

# ==========================================
# SCHEMAS PARA USUÁRIOS E AUTENTICAÇÃO
# ==========================================

class UsuarioBase(BaseModel):
    email: EmailStr # O Pydantic já valida automaticamente se tem "@" e ".com"
    objetivo: ObjetivoConta
    tipo_entidade: TipoEntidade
    nome_completo: str
    documento: str # Receberá o CPF ou CNPJ
    telefone: Optional[str] = None
    viu_guia_cadastro: bool = False

class UsuarioCreate(UsuarioBase):
    senha: str # A senha viaja limpa do Front-end para a Rota (via HTTPS)

class UsuarioResponse(UsuarioBase):
    id: int
    is_ativo: bool
    is_verificado: bool
    # Repare que NÃO incluímos o campo "senha" aqui. Ele nunca volta para o Front-end.

    model_config = ConfigDict(from_attributes=True)