from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# ==========================================
# SCHEMAS PARA EMPRESA (Locadora)
# ==========================================

# 1. Atributos base que toda Empresa tem
class EmpresaBase(BaseModel):
    razao_social: str
    cnpj: str
    email: EmailStr  # O Pydantic valida automaticamente se é um e-mail real
    telefone: Optional[str] = None

# 2. Dados exigidos no momento de CADASTRAR uma Empresa
class EmpresaCreate(EmpresaBase):
    pass # No futuro, se tivermos "senha", ela entra aqui (vem da internet, mas não volta)

# 3. Dados que DEVOLVEMOS para o Front-end após salvar no banco
class EmpresaResponse(EmpresaBase):
    id: int
    ativo: bool
    data_cadastro: datetime

    # Configuração vital: Ensina o Pydantic a ler os dados do SQLAlchemy (ORM)
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# SCHEMAS PARA CLIENTE (Locatário)
# ==========================================

class ClienteBase(BaseModel):
    nome_completo: str
    documento: str # Pode ser CPF ou CNPJ
    email: EmailStr
    telefone: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    ativo: bool
    data_cadastro: datetime

    model_config = ConfigDict(from_attributes=True)