"""
repository.py — Operações de acesso ao banco de dados para a entidade Analise.

Todas as funções recebem e retornam dicionários Python para desacoplamento
dos schemas FastAPI.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .connection import get_db


def _now_iso() -> str:
    """Retorna o momento atual em formato ISO 8601 UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _row_to_dict(row) -> Dict[str, Any]:
    """Converte um sqlite3.Row em dicionário Python."""
    return dict(row)


# ──────────────────────────────────────────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────────────────────────────────────────

def insert_analysis(
    name: str,
    description: Optional[str],
    target_path: str,
    score: Optional[float],
    report_path: Optional[str],
    status: str,
    summary: Optional[str],
) -> Dict[str, Any]:
    """Insere uma nova análise e retorna o registro completo."""
    now = _now_iso()
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO analyses
                (name, description, target_path, score, report_path, status, summary, created_at, updated_at)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (name, description, target_path, score, report_path, status, summary, now, now),
        )
        new_id = cursor.lastrowid

    return get_analysis_by_id(new_id)


# ──────────────────────────────────────────────────────────────────────────────
# READ
# ──────────────────────────────────────────────────────────────────────────────

def list_analyses() -> List[Dict[str, Any]]:
    """Retorna todas as análises, da mais recente para a mais antiga."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM analyses ORDER BY created_at DESC"
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def get_analysis_by_id(analysis_id: int) -> Optional[Dict[str, Any]]:
    """Retorna uma análise pelo ID, ou None se não encontrada."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM analyses WHERE id = ?",
            (analysis_id,),
        ).fetchone()
    return _row_to_dict(row) if row else None


# ──────────────────────────────────────────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────────────────────────────────────────

def update_analysis_fields(
    analysis_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    target_path: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Atualiza apenas os campos fornecidos (name, description, target_path).
    Retorna o registro atualizado, ou None se não encontrado.
    """
    fields: List[str] = []
    values: List[Any] = []

    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if target_path is not None:
        fields.append("target_path = ?")
        values.append(target_path)

    if not fields:
        return get_analysis_by_id(analysis_id)

    fields.append("updated_at = ?")
    values.append(_now_iso())
    values.append(analysis_id)

    with get_db() as conn:
        conn.execute(
            f"UPDATE analyses SET {', '.join(fields)} WHERE id = ?",
            values,
        )

    return get_analysis_by_id(analysis_id)


def update_analysis_result(
    analysis_id: int,
    score: float,
    report_path: str,
    status: str,
    summary: str,
) -> Optional[Dict[str, Any]]:
    """
    Atualiza os campos de resultado de uma análise após re-execução.
    Retorna o registro atualizado, ou None se não encontrado.
    """
    with get_db() as conn:
        conn.execute(
            """
            UPDATE analyses
               SET score = ?, report_path = ?, status = ?, summary = ?, updated_at = ?
             WHERE id = ?
            """,
            (score, report_path, status, summary, _now_iso(), analysis_id),
        )
    return get_analysis_by_id(analysis_id)


# ──────────────────────────────────────────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────────────────────────────────────────

def delete_analysis(analysis_id: int) -> bool:
    """
    Exclui o registro da análise do banco.
    Retorna True se o registro existia e foi removido, False caso contrário.
    NÃO exclui a pasta original analisada nem o relatório gerado.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM analyses WHERE id = ?",
            (analysis_id,),
        )
    return cursor.rowcount > 0
