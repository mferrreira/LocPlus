import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Passo 1: Mandar o Python ler o nosso cofre de senhas (.env)
load_dotenv()

# Passo 2: Puxar a URL de conexão exata que você colou lá
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Passo 3: Criar o Motor (Engine) que vai conversar com o PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Passo 4: Criar uma "Fábrica de Sessões" (Cada vez que o usuário acessar o site, abre uma sessão rápida)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Passo 5: Criar a Base (Nossas futuras tabelas de Empresas e Máquinas herdarão disso)
Base = declarative_base()

# Função auxiliar para injetarmos o banco de dados nas nossas rotas depois
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()