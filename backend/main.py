"""
CAW Ops Intelligence - Backend API + Frontend
Sistema de Gestão Operacional e Inteligência de Risco

Desenvolvido para demonstrar capacidades de desenvolvimento de sistemas
com visão de negócio e análise de dados operacionais.
"""

import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import engine, Base
from routes import auth, projects, dashboard

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CAW Ops Intelligence API",
    description="API do Sistema de Gestão Operacional e Inteligência de Risco - CAW Telecom e Energia",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas da API
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(dashboard.router)


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "CAW Ops Intelligence"}


# Servir frontend compilado (dist)
# Compatível com estrutura local e Docker/Render
_local_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
_docker_dist = Path("/app/frontend/dist")
FRONTEND_DIR = _docker_dist if _docker_dist.exists() else _local_dist

if FRONTEND_DIR.exists():
    # Montar arquivos estáticos (assets, imagens, etc.)
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="static-assets")

    @app.get("/caw-logo.png")
    async def serve_logo():
        return FileResponse(str(FRONTEND_DIR / "caw-logo.png"))

    @app.get("/caw-logo-dark.jpg")
    async def serve_logo_dark():
        return FileResponse(str(FRONTEND_DIR / "caw-logo-dark.jpg"))

    # Catch-all: qualquer rota que não seja /api/* serve o index.html (SPA)
    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # Se o path começa com 'api', não interceptar
        if full_path.startswith("api"):
            return {"detail": "Not Found"}
        
        # Verificar se é um arquivo estático existente
        file_path = FRONTEND_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        
        # Caso contrário, servir index.html (Vue Router cuida da rota)
        return FileResponse(str(FRONTEND_DIR / "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
