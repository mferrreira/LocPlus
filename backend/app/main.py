from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importamos os roteadores
from app.api import usuarios
from app.api import clientes
from app.api import equipamentos
from app.api import locacoes
from app.api import enderecos
from app.api import vistorias

app = FastAPI(
    title="LocPlus API",
    description="Backend para gestão de locação de máquinas e vistorias",
    version="1.0.0"
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "sucesso",
        "sistema": "LocPlus",
        "mensagem": "Motor do backend rodando perfeitamente! 🚀"
    }

# Conectamos as rotas na API principal
app.include_router(usuarios.router)
app.include_router(clientes.router)
app.include_router(equipamentos.router)
app.include_router(locacoes.router)
app.include_router(enderecos.router)
app.include_router(vistorias.router)
