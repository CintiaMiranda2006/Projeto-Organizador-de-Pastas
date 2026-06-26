"""
score.py — Calcula a nota final de organização do projeto (0 a 10).

Critérios de pontuação (conforme PRD, seção 14):

| Critério                              | Máximo |
|---------------------------------------|-------:|
| Organização de pastas                 |   2 pt |
| Ausência de arquivos soltos           |   2 pt |
| Ausência de arquivos vazios           |   1 pt |
| Ausência de pastas vazias             |   1 pt |
| Padrão de nomes                       |   2 pt |
| Uso correto de timestamp              |   1 pt |
| Coerência entre ordem e timestamp     |   1 pt |
| TOTAL                                 |  10 pt |
"""

from dataclasses import dataclass, field
from typing import List

from .file_scanner import ScanResult
from .timestamp_checker import TimestampResult
from .order_checker import OrderIssue


@dataclass
class ScoreBreakdown:
    """Detalhamento da pontuação por critério."""
    pasta_organization: float = 0.0      # máx 2
    loose_files: float = 0.0            # máx 2
    empty_files: float = 0.0            # máx 1
    empty_dirs: float = 0.0             # máx 1
    naming_pattern: float = 0.0         # máx 2
    timestamp_usage: float = 0.0        # máx 1
    order_coherence: float = 0.0        # máx 1
    total: float = 0.0
    details: List[str] = field(default_factory=list)


def calculate_score(
    scan_result: ScanResult,
    loose_files: List[str],
    empty_files: List[str],
    empty_dirs: List[str],
    invalid_pattern: List[str],
    generic_names: List[str],
    mixed_separators: List[str],
    timestamp_results: List[TimestampResult],
    order_issues: List[OrderIssue],
) -> ScoreBreakdown:
    """
    Calcula a nota de 0 a 10 com base nos critérios do PRD.
    """
    bd = ScoreBreakdown()
    total_files = len(scan_result.files)
    total_dirs = len(scan_result.dirs)

    # ─── 1. Organização de pastas (2 pt) ─────────────────────────────────────
    # Pontuação máxima se há pelo menos uma subpasta e os arquivos estão
    # distribuídos nelas. Penaliza proporcionalmente à proporção de arquivos soltos.
    if total_dirs == 0:
        # Projeto sem pastas: penalidade total
        bd.pasta_organization = 0.0
        bd.details.append("Organização de pastas: 0/2 — Nenhuma subpasta encontrada.")
    else:
        # Quanto mais arquivos soltos em relação ao total, menor a nota
        loose_ratio = len(loose_files) / total_files if total_files > 0 else 0
        bd.pasta_organization = round(2.0 * (1 - loose_ratio), 2)
        bd.details.append(
            f"Organização de pastas: {bd.pasta_organization}/2 — "
            f"{total_dirs} pasta(s), {len(loose_files)} arquivo(s) solto(s)."
        )

    # ─── 2. Ausência de arquivos soltos (2 pt) ───────────────────────────────
    if total_files == 0:
        bd.loose_files = 2.0
    else:
        loose_ratio = len(loose_files) / total_files
        bd.loose_files = round(2.0 * (1 - loose_ratio), 2)

    bd.details.append(
        f"Arquivos soltos: {bd.loose_files}/2 — "
        f"{len(loose_files)} arquivo(s) solto(s) de {total_files}."
    )

    # ─── 3. Ausência de arquivos vazios (1 pt) ───────────────────────────────
    if total_files == 0:
        bd.empty_files = 1.0
    else:
        empty_ratio = len(empty_files) / total_files
        bd.empty_files = round(1.0 * (1 - empty_ratio), 2)

    bd.details.append(
        f"Arquivos vazios: {bd.empty_files}/1 — "
        f"{len(empty_files)} arquivo(s) vazio(s) de {total_files}."
    )

    # ─── 4. Ausência de pastas vazias (1 pt) ─────────────────────────────────
    if total_dirs == 0:
        bd.empty_dirs = 1.0
    else:
        empty_dir_ratio = len(empty_dirs) / total_dirs
        bd.empty_dirs = round(1.0 * (1 - empty_dir_ratio), 2)

    bd.details.append(
        f"Pastas vazias: {bd.empty_dirs}/1 — "
        f"{len(empty_dirs)} pasta(s) vazia(s) de {total_dirs}."
    )

    # ─── 5. Padrão de nomes (2 pt) ──────────────────────────────────────────
    # Penaliza por arquivos fora do padrão, genéricos e com separador misto
    name_issues = set(invalid_pattern) | set(generic_names) | set(mixed_separators)
    if total_files == 0:
        bd.naming_pattern = 2.0
    else:
        name_issue_ratio = len(name_issues) / total_files
        bd.naming_pattern = round(2.0 * (1 - name_issue_ratio), 2)

    bd.details.append(
        f"Padrão de nomes: {bd.naming_pattern}/2 — "
        f"{len(name_issues)} arquivo(s) com problema(s) de nome."
    )

    # ─── 6. Uso correto de timestamp (1 pt) ──────────────────────────────────
    missing_ts = [r for r in timestamp_results if not r.has_timestamp]
    invalid_ts = [r for r in timestamp_results if r.has_timestamp and not r.is_valid]
    ts_issues = len(missing_ts) + len(invalid_ts)

    if total_files == 0:
        bd.timestamp_usage = 1.0
    else:
        ts_ratio = ts_issues / total_files
        bd.timestamp_usage = round(1.0 * (1 - ts_ratio), 2)

    bd.details.append(
        f"Timestamp: {bd.timestamp_usage}/1 — "
        f"{len(missing_ts)} sem timestamp, {len(invalid_ts)} com timestamp inválido."
    )

    # ─── 7. Coerência entre ordem e timestamp (1 pt) ─────────────────────────
    # Penaliza proporcionalmente ao número de arquivos com ordem incoerente
    # em relação ao total de arquivos com letra de ordem
    files_with_order = [
        f for f in scan_result.files
        if len(f.name) > 1 and f.name[1] in ('_', '-') and f.name[0].isalpha()
    ]
    n_ordered = len(files_with_order)

    if n_ordered == 0:
        bd.order_coherence = 1.0
        bd.details.append("Coerência de ordem: 1/1 — Nenhum arquivo com letra de ordem.")
    else:
        order_ratio = len(order_issues) / n_ordered
        bd.order_coherence = round(1.0 * (1 - order_ratio), 2)
        bd.details.append(
            f"Coerência de ordem: {bd.order_coherence}/1 — "
            f"{len(order_issues)} inconsistência(s) de ordem."
        )

    # ─── Total ────────────────────────────────────────────────────────────────
    bd.total = round(
        bd.pasta_organization
        + bd.loose_files
        + bd.empty_files
        + bd.empty_dirs
        + bd.naming_pattern
        + bd.timestamp_usage
        + bd.order_coherence,
        1,
    )

    return bd

