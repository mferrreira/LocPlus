from pydantic import BaseModel, ConfigDict

class EmpresaBase(BaseModel):
    razao_social: str
    cnpj: str

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)