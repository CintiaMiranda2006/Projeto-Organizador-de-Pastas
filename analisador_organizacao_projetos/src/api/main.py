"""
main.py — Ponto de entrada da aplicação FastAPI.

Para rodar:
    py -m uvicorn src.api.main:app --reload

Documentação interativa:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.database.init_db import init_db
from src.api.routes import router

# ── Aplicação ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Analisador de Organização de Projetos — API",
    description=(
        "API REST para criar, listar, visualizar, atualizar, re-executar "
        "e excluir análises de organização de pastas de projeto."
    ),
    version="1.0.0",
    contact={
        "name": "Analisador de Organização de Projetos",
    },
)

# ── CORS — permite chamadas do frontend HTML local (file://) ──────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Inicialização do banco ─────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup() -> None:
    """Cria as tabelas do banco ao iniciar a aplicação (idempotente)."""
    init_db()

# ── Rotas ─────────────────────────────────────────────────────────────────────
app.include_router(router)


# ── Rota de saúde ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict:
    return {
        "status": "ok",
        "message": "Analisador de Organização de Projetos — API rodando.",
        "docs": "/docs",
        "frontend": "/app",
    }


# ── Frontend estático ──────────────────────────────────────────────────────────
# Servido em /app — acessível em http://127.0.0.1:8000/app/
import os as _os
_FRONTEND_DIR = _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "frontend"
)
app.mount("/app", StaticFiles(directory=_FRONTEND_DIR, html=True), name="frontend")


# ── Rota raiz ─────────────────────────────────────────────────────────────────
from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/app/pages/index.html")

