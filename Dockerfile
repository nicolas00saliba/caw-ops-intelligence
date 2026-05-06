# ============================================
# CAW Ops Intelligence - Dockerfile para Render.com
# Build multi-stage: Node (frontend) + Python (backend)
# ============================================

# --- Stage 1: Build do Frontend ---
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Copiar arquivos de dependência primeiro (cache de camadas)
COPY frontend/package.json frontend/pnpm-lock.yaml* frontend/package-lock.json* ./

# Instalar dependências (--legacy-peer-deps para resolver conflito apexcharts)
RUN npm install --legacy-peer-deps

# Copiar código-fonte do frontend
COPY frontend/ ./

# Build de produção
RUN npm run build

# --- Stage 2: Backend Python + Frontend compilado ---
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/ ./backend/

# Copiar frontend compilado do stage anterior
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Gerar o banco de dados com dados fictícios
WORKDIR /app/backend
RUN python seed.py

# Expor porta (Render usa a variável PORT)
EXPOSE 8000

# Comando de inicialização
CMD ["sh", "-c", "cd /app/backend && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
