from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Injeção Crítica: Carrega todas as instâncias do DB no ambiente (Pre-Requisito SQLAlchemy)
import app.models  # Força a inicialização do __init__.py!

# Importamos os roteadores
from app.api import usuarios, empresas, clientes, equipamentos, locacoes, vistorias, enderecos, kyc, catalogo

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
app.include_router(empresas.router)
app.include_router(clientes.router)
app.include_router(equipamentos.router)
app.include_router(locacoes.router)
app.include_router(vistorias.router)
app.include_router(enderecos.router)
app.include_router(kyc.router)
app.include_router(catalogo.router)
