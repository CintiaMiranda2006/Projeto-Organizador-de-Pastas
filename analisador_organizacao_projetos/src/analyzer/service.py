"""
service.py — Serviço de análise reutilizável pela API.

Encapsula o fluxo completo do analisador (scan → checkers → score → report)
em uma única função chamável como biblioteca, sem depender do terminal.
"""

import json
import os
from dataclasses import dataclass
from typing import Optional

from .file_scanner import scan
from .naming_checker import check_naming
from .timestamp_checker import check_timestamps
from .order_checker import check_order
from .empty_checker import check_empty_files, check_empty_dirs
from .loose_file_checker import check_loose_files
from .score import calculate_score
from .report import generate_report


@dataclass
class AnalysisResult:
    """Resultado da análise retornado para a API."""
    score: float
    report_path: str
    status: str           # "completed" | "error"
    summary: str          # JSON string com resumo dos problemas
    error_message: Optional[str] = None


def run_analysis(target_path: str) -> AnalysisResult:
    """
    Executa a análise completa de uma pasta e retorna um AnalysisResult.

    Parâmetros:
        target_path: caminho absoluto ou relativo da pasta a ser analisada.

    Retorna:
        AnalysisResult com nota, caminho do relatório, status e resumo.
    """
    try:
        abs_path = os.path.abspath(target_path)

        if not os.path.isdir(abs_path):
            return AnalysisResult(
                score=0.0,
                report_path="",
                status="error",
                summary=json.dumps({"error": f"Caminho não encontrado ou não é uma pasta: {abs_path}"}),
                error_message=f"Caminho não encontrado ou não é uma pasta: {abs_path}",
            )

        # 1. Escanear
        scan_result = scan(abs_path)

        # 2. Verificações
        loose_files = check_loose_files(scan_result)
        empty_files = check_empty_files(scan_result.files)
        empty_dirs = check_empty_dirs(scan_result)
        invalid_pattern, generic_names, mixed_separators, _ = check_naming(scan_result.files)
        timestamp_results = check_timestamps(scan_result.files)
        order_issues = check_order(scan_result.files)

        # 3. Nota
        score = calculate_score(
            scan_result,
            loose_files,
            empty_files,
            empty_dirs,
            invalid_pattern,
            generic_names,
            mixed_separators,
            timestamp_results,
            order_issues,
        )

        # 4. Relatório
        report_path = generate_report(
            scan_result,
            loose_files,
            empty_files,
            empty_dirs,
            invalid_pattern,
            generic_names,
            mixed_separators,
            timestamp_results,
            order_issues,
            score,
        )

        # 5. Resumo estruturado dos problemas (salvo como JSON no banco)
        missing_ts_list = [r.rel_path for r in timestamp_results if not r.has_timestamp]
        invalid_ts_list = [
            f"{r.rel_path} — {r.error}"
            for r in timestamp_results
            if r.has_timestamp and not r.is_valid
        ]
        order_issues_list = [
            f"{oi.rel_path} — {oi.description}" for oi in order_issues
        ]

        summary_dict = {
            "total_files": len(scan_result.files),
            "total_dirs": len(scan_result.dirs),
            # ── Contagens (para badges de quantidade) ──
            "loose_files": len(loose_files),
            "empty_files": len(empty_files),
            "empty_dirs": len(empty_dirs),
            "invalid_pattern": len(invalid_pattern),
            "generic_names": len(generic_names),
            "mixed_separators": len(mixed_separators),
            "missing_timestamps": len(missing_ts_list),
            "invalid_timestamps": len(invalid_ts_list),
            "order_issues": len(order_issues_list),
            # ── Listas de arquivos/pastas com problema ──
            "lista_arquivos_soltos": loose_files,
            "lista_arquivos_vazios": empty_files,
            "lista_pastas_vazias": empty_dirs,
            "lista_fora_do_padrao": invalid_pattern,
            "lista_nomes_genericos": generic_names,
            "lista_separadores_inconsistentes": mixed_separators,
            "lista_sem_timestamp": missing_ts_list,
            "lista_timestamp_invalido": invalid_ts_list,
            "lista_ordem_incoerente": order_issues_list,
            # ── Pontuação por critério (em português) ──
            "pontuacao_por_criterio": {
                "Organização de pastas": score.pasta_organization,
                "Arquivos soltos": score.loose_files,
                "Arquivos vazios": score.empty_files,
                "Pastas vazias": score.empty_dirs,
                "Padrão de nomes": score.naming_pattern,
                "Uso de timestamp": score.timestamp_usage,
                "Coerência de ordem": score.order_coherence,
            },
        }

        return AnalysisResult(
            score=score.total,
            report_path=report_path,
            status="completed",
            summary=json.dumps(summary_dict, ensure_ascii=False),
        )

    except Exception as exc:
        return AnalysisResult(
            score=0.0,
            report_path="",
            status="error",
            summary=json.dumps({"error": str(exc)}),
            error_message=str(exc),
        )
