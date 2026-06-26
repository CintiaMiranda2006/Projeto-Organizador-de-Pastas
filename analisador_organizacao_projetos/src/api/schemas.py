"""
schemas.py — Modelos Pydantic de entrada e saída da API.

Separados em:
  - AnalysisCreate : corpo da requisição POST /analyses
  - AnalysisUpdate : corpo da requisição PUT /analyses/{id}
  - AnalysisSummary: resposta compacta para listagem
  - AnalysisDetail : resposta completa com todos os campos
"""

import json
from typing import Any, Dict, Optional

from pydantic import BaseModel, field_validator


# ──────────────────────────────────────────────────────────────────────────────
# Entrada
# ──────────────────────────────────────────────────────────────────────────────

class AnalysisCreate(BaseModel):
    """Dados necessários para criar uma nova análise."""
    name: str
    description: Optional[str] = None
    target_path: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O campo 'name' não pode ser vazio.")
        return v.strip()

    @field_validator("target_path")
    @classmethod
    def target_path_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O campo 'target_path' não pode ser vazio.")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Análise do projeto X",
                    "description": "Verificar organização dos PRDs",
                    "target_path": "./samples/projeto_organizado",
                }
            ]
        }
    }


class AnalysisUpdate(BaseModel):
    """Campos editáveis de uma análise (todos opcionais)."""
    name: Optional[str] = None
    description: Optional[str] = None
    target_path: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Novo nome da análise",
                    "description": "Descrição atualizada",
                    "target_path": "./samples/projeto_baguncado",
                }
            ]
        }
    }


# ──────────────────────────────────────────────────────────────────────────────
# Saída
# ──────────────────────────────────────────────────────────────────────────────

class AnalysisSummary(BaseModel):
    """Resposta compacta usada na listagem."""
    id: int
    name: str
    description: Optional[str]
    target_path: str
    score: Optional[float]
    status: str
    created_at: str
    updated_at: str


class AnalysisDetail(BaseModel):
    """Resposta completa retornada ao buscar por ID."""
    id: int
    name: str
    description: Optional[str]
    target_path: str
    score: Optional[float]
    report_path: Optional[str]
    status: str
    summary: Optional[Dict[str, Any]]   # desserializado do JSON armazenado
    created_at: str
    updated_at: str

    @classmethod
    def from_db_row(cls, row: dict) -> "AnalysisDetail":
        """Constrói um AnalysisDetail a partir de um dicionário do banco."""
        summary_raw = row.get("summary")
        summary_parsed: Optional[Dict[str, Any]] = None
        if summary_raw:
            try:
                summary_parsed = json.loads(summary_raw)
            except (json.JSONDecodeError, TypeError):
                summary_parsed = {"raw": summary_raw}

        return cls(
            id=row["id"],
            name=row["name"],
            description=row.get("description"),
            target_path=row["target_path"],
            score=row.get("score"),
            report_path=row.get("report_path"),
            status=row["status"],
            summary=summary_parsed,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
