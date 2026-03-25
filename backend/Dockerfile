# Usa uma versão oficial e enxuta do Python para economizar RAM
FROM python:3.12-slim

# Define a pasta principal lá dentro do container
WORKDIR /app

# Variáveis de ambiente para otimizar o Python no Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema operacional que alguns pacotes Python exigem
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala primeiro os requirements (Isso usa o cache do Docker e deixa os próximos builds mega rápidos)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código da sua máquina para dentro do container
COPY . .