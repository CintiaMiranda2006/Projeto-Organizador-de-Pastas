"""
init_db.py — Cria as tabelas do banco de dados se ainda não existirem.

Deve ser chamado uma vez na inicialização da aplicação (main.py).
"""

from .connection import get_db

CREATE_ANALYSES_TABLE = """
CREATE TABLE IF NOT EXISTS analyses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    description  TEXT,
    target_path  TEXT    NOT NULL,
    score        REAL,
    report_path  TEXT,
    status       TEXT    NOT NULL DEFAULT 'pending',
    summary      TEXT,
    created_at   TEXT    NOT NULL,
    updated_at   TEXT    NOT NULL
);
"""


def init_db() -> None:
    """Cria todas as tabelas necessárias, se ainda não existirem."""
    with get_db() as conn:
        conn.execute(CREATE_ANALYSES_TABLE)
