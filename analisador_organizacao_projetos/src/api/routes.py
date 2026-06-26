"""
routes.py — Rotas do CRUD de análises.

Endpoints:
  POST   /analyses                  Criar e executar análise
  GET    /analyses                  Listar análises
  GET    /analyses/{id}             Buscar análise por ID
  PUT    /analyses/{id}             Atualizar nome, descrição ou caminho
  POST   /analyses/{id}/rerun       Re-executar análise
  DELETE /analyses/{id}             Excluir análise
"""

import os
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.analyzer.service import run_analysis
from src.database import repository
from .schemas import AnalysisCreate, AnalysisDetail, AnalysisSummary, AnalysisUpdate

router = APIRouter(prefix="/analyses", tags=["analyses"])


# ──────────────────────────────────────────────────────────────────────────────
# POST /analyses — Criar análise
# ──────────────────────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=AnalysisDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Criar e executar análise",
    description=(
        "Cadastra uma nova análise. Executa automaticamente o analisador "
        "na pasta informada e salva o resultado no banco."
    ),
)
def create_analysis(body: AnalysisCreate) -> AnalysisDetail:
    target = os.path.abspath(body.target_path)

    # Executa o analisador (caminho inválido gera status='error' internamente)
    result = run_analysis(target)

    row = repository.insert_analysis(
        name=body.name,
        description=body.description,
        target_path=target,
        score=result.score,
        report_path=result.report_path,
        status=result.status,
        summary=result.summary,
    )
    return AnalysisDetail.from_db_row(row)


# ──────────────────────────────────────────────────────────────────────────────
# GET /analyses — Listar análises
# ──────────────────────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=List[AnalysisSummary],
    summary="Listar análises",
    description="Retorna todas as análises cadastradas, da mais recente para a mais antiga.",
)
def list_analyses() -> List[AnalysisSummary]:
    rows = repository.list_analyses()
    return [AnalysisSummary(**r) for r in rows]


# ──────────────────────────────────────────────────────────────────────────────
# GET /analyses/{id} — Buscar por ID
# ──────────────────────────────────────────────────────────────────────────────

@router.get(
    "/{analysis_id}",
    response_model=AnalysisDetail,
    summary="Buscar análise por ID",
    description="Retorna todos os campos de uma análise, incluindo nota e resumo dos problemas.",
)
def get_analysis(analysis_id: int) -> AnalysisDetail:
    row = repository.get_analysis_by_id(analysis_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Análise com id={analysis_id} não encontrada.",
        )
    return AnalysisDetail.from_db_row(row)


# ──────────────────────────────────────────────────────────────────────────────
# PUT /analyses/{id} — Atualizar campos
# ──────────────────────────────────────────────────────────────────────────────

@router.put(
    "/{analysis_id}",
    response_model=AnalysisDetail,
    summary="Atualizar análise",
    description=(
        "Atualiza nome, descrição e/ou caminho da análise. "
        "Não re-executa o analisador automaticamente."
    ),
)
def update_analysis(analysis_id: int, body: AnalysisUpdate) -> AnalysisDetail:
    existing = repository.get_analysis_by_id(analysis_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Análise com id={analysis_id} não encontrada.",
        )

    target_path = os.path.abspath(body.target_path) if body.target_path else None

    row = repository.update_analysis_fields(
        analysis_id=analysis_id,
        name=body.name,
        description=body.description,
        target_path=target_path,
    )
    return AnalysisDetail.from_db_row(row)


# ──────────────────────────────────────────────────────────────────────────────
# POST /analyses/{id}/rerun — Re-executar análise
# ──────────────────────────────────────────────────────────────────────────────

@router.post(
    "/{analysis_id}/rerun",
    response_model=AnalysisDetail,
    summary="Re-executar análise",
    description=(
        "Executa novamente o analisador sobre o caminho salvo na análise. "
        "Atualiza nota, resumo, relatório e status."
    ),
)
def rerun_analysis(analysis_id: int) -> AnalysisDetail:
    existing = repository.get_analysis_by_id(analysis_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Análise com id={analysis_id} não encontrada.",
        )

    result = run_analysis(existing["target_path"])

    row = repository.update_analysis_result(
        analysis_id=analysis_id,
        score=result.score,
        report_path=result.report_path,
        status=result.status,
        summary=result.summary,
    )
    return AnalysisDetail.from_db_row(row)


# ──────────────────────────────────────────────────────────────────────────────
# DELETE /analyses/{id} — Excluir análise
# ──────────────────────────────────────────────────────────────────────────────

@router.delete(
    "/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir análise",
    description=(
        "Remove o registro da análise do banco de dados. "
        "NÃO exclui a pasta original analisada nem o relatório gerado."
    ),
)
def delete_analysis(analysis_id: int) -> None:
    deleted = repository.delete_analysis(analysis_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Análise com id={analysis_id} não encontrada.",
        )
