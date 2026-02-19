# LocPlus

Infra inicial do SaaS de locacao de maquinas.

## Stack
- Frontend: React + Vite
- Backend: FastAPI + SQLAlchemy + Alembic
- Banco: PostgreSQL
- Bucket: MinIO
- Gateway: Nginx

## Pre-requisitos
- Docker
- Docker Compose (plugin `docker compose`)

## Setup rapido
1. Copie o arquivo de exemplo (se necessario):
   - `cp .env.example .env`
2. Suba a stack:
   - `docker compose up --build -d`

## Endpoints locais
- App (via gateway): `http://localhost`
- API healthcheck: `http://localhost/api/healthz`
- MinIO API: `http://localhost:9000`
- MinIO Console: `http://localhost:9001`
- PostgreSQL: `localhost:5432`

## Comandos uteis
- Ver status: `docker compose ps`
- Ver logs backend: `docker compose logs -f backend`
- Derrubar stack: `docker compose down`
