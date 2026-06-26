"""
connection.py — Gerencia a conexão com o banco de dados SQLite.

O arquivo do banco é criado automaticamente na raiz do projeto
como `database.db`, ao lado de requirements.txt e README.md.
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Generator

# Localização do banco: raiz do projeto (dois níveis acima de src/database/)
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
DB_PATH = os.path.join(_PROJECT_ROOT, "database.db")


def get_raw_connection() -> sqlite3.Connection:
    """
    Retorna uma conexão SQLite com Row Factory habilitado
    (permite acessar colunas por nome: row["id"]).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # melhor performance em leituras concorrentes
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager que abre, fornece e fecha automaticamente uma conexão.

    Uso:
        with get_db() as conn:
            conn.execute(...)
    """
    conn = get_raw_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
