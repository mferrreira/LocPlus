from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from typing import Optional
from datetime import date
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
    telefone_celular: Optional[str] = None
    telefone_fixo: Optional[str] = None
    
    # Campos PF
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None
    
    viu_guia_cadastro: bool = False

    @model_validator(mode='after')
    def check_pf_requirements(self):
        if self.tipo_entidade == TipoEntidade.PF:
            if not self.rg:
                raise ValueError("RG é obrigatório para Pessoa Física")
            if not self.data_nascimento:
                raise ValueError("Data de Nascimento é obrigatória para Pessoa Física")
        return self

class UsuarioCreate(UsuarioBase):
    senha: str # A senha viaja limpa do Front-end para a Rota (via HTTPS)
    # Campos PJ agora no Create
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    inscricao_estadual: Optional[str] = None

    @model_validator(mode='after')
    def check_pj_requirements(self):
        if self.tipo_entidade == TipoEntidade.PJ:
            if not self.razao_social:
                raise ValueError("Razão Social é obrigatória para Pessoa Jurídica")
            if not self.nome_fantasia:
                raise ValueError("Nome Fantasia é obrigatório para Pessoa Jurídica")
            if not self.inscricao_estadual:
                raise ValueError("Inscrição Estadual é obrigatória para Pessoa Jurídica")
        return self

class UsuarioResponse(UsuarioBase):
    id: int
    is_ativo: bool
    is_verificado: bool
    # Repare que NÃO incluímos o campo "senha" aqui. Ele nunca volta para o Front-end.

    model_config = ConfigDict(from_attributes=True)