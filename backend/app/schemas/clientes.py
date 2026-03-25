from pydantic import BaseModel, ConfigDict

class ClienteBase(BaseModel):
    nome: str
    documento: str

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)