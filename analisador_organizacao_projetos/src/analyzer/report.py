"""
report.py — Gera o relatório final em Markdown a partir dos resultados da análise.

O relatório é salvo na pasta `reports/` do projeto analisador (não da pasta analisada).
"""

import os
from datetime import datetime
from collections import Counter
from typing import List

from .file_scanner import ScanResult
from .timestamp_checker import TimestampResult
from .order_checker import OrderIssue
from .score import ScoreBreakdown


# Caminho base dos relatórios: pasta reports/ na raiz do projeto
# src/analyzer/ → src/ → project_root/ → reports/
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
_REPORTS_DIR = os.path.join(_SRC_DIR, "..", "..", "reports")


def _safe_reports_dir() -> str:
    """Garante que a pasta reports/ existe e retorna o caminho absoluto."""
    reports_path = os.path.abspath(_REPORTS_DIR)
    os.makedirs(reports_path, exist_ok=True)
    return reports_path


def _score_emoji(score: float) -> str:
    if score >= 9:
        return "🟢"
    if score >= 7:
        return "🟡"
    if score >= 5:
        return "🟠"
    return "🔴"


def _list_section(title: str, items: List[str], empty_msg: str = "Nenhum.") -> str:
    """Formata uma seção de lista Markdown."""
    lines = [f"### {title}", ""]
    if items:
        for item in items:
            lines.append(f"- `{item}`")
    else:
        lines.append(f"_{empty_msg}_")
    lines.append("")
    return "\n".join(lines)


def generate_report(
    scan_result: ScanResult,
    loose_files: List[str],
    empty_files: List[str],
    empty_dirs: List[str],
    invalid_pattern: List[str],
    generic_names: List[str],
    mixed_separators: List[str],
    timestamp_results: List[TimestampResult],
    order_issues: List[OrderIssue],
    score: ScoreBreakdown,
) -> str:
    """
    Gera o relatório em Markdown e salva em reports/.
    Retorna o caminho absoluto do arquivo gerado.
    """
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    project_name = scan_result.root_name
    emoji = _score_emoji(score.total)

    # ── Separar timestamps com problema ──────────────────────────────────────
    missing_ts = [r.rel_path for r in timestamp_results if not r.has_timestamp]
    invalid_ts = [
        f"{r.rel_path} — {r.error}"
        for r in timestamp_results
        if r.has_timestamp and not r.is_valid
    ]

    # ── Tipos de arquivo encontrados ─────────────────────────────────────────
    ext_counter: Counter = Counter(f.extension for f in scan_result.files if f.extension)
    ext_summary = ", ".join(
        f"`{ext}` ({count})" for ext, count in ext_counter.most_common()
    ) or "_Nenhuma extensão identificada._"

    # ── Pontos positivos ──────────────────────────────────────────────────────
    positives: List[str] = []
    if not loose_files:
        positives.append("Nenhum arquivo solto na raiz.")
    if not empty_files:
        positives.append("Nenhum arquivo vazio.")
    if not empty_dirs:
        positives.append("Nenhuma pasta vazia.")
    if not invalid_pattern and not generic_names and not mixed_separators:
        positives.append("Todos os arquivos seguem o padrão de nomes.")
    if not missing_ts and not invalid_ts:
        positives.append("Todos os timestamps estão corretos.")
    if not order_issues:
        positives.append("A ordem cronológica dos arquivos está coerente.")
    if not positives:
        positives.append("Nenhum ponto positivo identificado. Há muito a melhorar!")

    # ── Sugestões ─────────────────────────────────────────────────────────────
    suggestions: List[str] = []
    if loose_files:
        suggestions.append(
            "Mova os arquivos soltos para subpastas organizadas por tema ou tipo."
        )
    if empty_files:
        suggestions.append(
            "Remova ou preencha os arquivos vazios encontrados."
        )
    if empty_dirs:
        suggestions.append(
            "Remova as pastas vazias ou adicione conteúdo relevante a elas."
        )
    if invalid_pattern or generic_names:
        suggestions.append(
            "Renomeie os arquivos seguindo o padrão: "
            "`ordem_tipo_assunto_aammdd_hhmm.extensao` "
            "(ex: `a_prd_login_260622_1430.md`)."
        )
    if mixed_separators:
        suggestions.append(
            "Padronize o separador em todos os arquivos: use `_` (underscore) "
            "ou `-` (hífen), mas nunca misture os dois."
        )
    if missing_ts:
        suggestions.append(
            "Adicione timestamp no formato `AAMMDD_HHMM` ao final dos nomes "
            "dos arquivos sem timestamp."
        )
    if invalid_ts:
        suggestions.append(
            "Corrija os timestamps inválidos: verifique mês (01–12), "
            "dia (01–31), hora (00–23) e minuto (00–59)."
        )
    if order_issues:
        suggestions.append(
            "Corrija a letra inicial dos arquivos para que reflita a ordem "
            "cronológica real (do mais antigo para o mais recente)."
        )
    if not suggestions:
        suggestions.append("Parabéns! Nenhuma sugestão necessária.")

    # ── Montar o relatório ────────────────────────────────────────────────────
    lines = [
        "# Relatório de Organização",
        "",
        f"## Projeto analisado",
        "",
        f"**{project_name}**",
        f"> Caminho: `{scan_result.root_path}`",
        "",
        f"## Nota final",
        "",
        f"### {emoji} {score.total}/10",
        "",
        "#### Detalhamento da pontuação",
        "",
        "| Critério | Pontuação | Máximo |",
        "|---|---:|---:|",
        f"| Organização de pastas | {score.pasta_organization} | 2 |",
        f"| Ausência de arquivos soltos | {score.loose_files} | 2 |",
        f"| Ausência de arquivos vazios | {score.empty_files} | 1 |",
        f"| Ausência de pastas vazias | {score.empty_dirs} | 1 |",
        f"| Padrão de nomes | {score.naming_pattern} | 2 |",
        f"| Uso correto de timestamp | {score.timestamp_usage} | 1 |",
        f"| Coerência entre ordem e timestamp | {score.order_coherence} | 1 |",
        f"| **Total** | **{score.total}** | **10** |",
        "",
        "## Visão geral",
        "",
        f"- **Data da análise:** {now}",
        f"- **Arquivos analisados:** {len(scan_result.files)}",
        f"- **Pastas analisadas:** {len(scan_result.dirs)}",
        f"- **Tipos de arquivo:** {ext_summary}",
        "",
        "## Problemas encontrados",
        "",
    ]

    lines.append(
        _list_section(
            f"Arquivos soltos ({len(loose_files)})",
            loose_files,
            "Nenhum arquivo solto.",
        )
    )
    lines.append(
        _list_section(
            f"Arquivos vazios ({len(empty_files)})",
            empty_files,
            "Nenhum arquivo vazio.",
        )
    )
    lines.append(
        _list_section(
            f"Pastas vazias ({len(empty_dirs)})",
            empty_dirs,
            "Nenhuma pasta vazia.",
        )
    )
    lines.append(
        _list_section(
            f"Arquivos fora do padrão de nome ({len(invalid_pattern)})",
            invalid_pattern,
            "Todos os arquivos seguem o padrão.",
        )
    )
    lines.append(
        _list_section(
            f"Arquivos com nome genérico ({len(generic_names)})",
            generic_names,
            "Nenhum nome genérico encontrado.",
        )
    )
    lines.append(
        _list_section(
            f"Arquivos com separador inconsistente ({len(mixed_separators)})",
            mixed_separators,
            "Separadores consistentes.",
        )
    )
    lines.append(
        _list_section(
            f"Arquivos sem timestamp ({len(missing_ts)})",
            missing_ts,
            "Todos os arquivos possuem timestamp.",
        )
    )
    lines.append(
        _list_section(
            f"Arquivos com timestamp inválido ({len(invalid_ts)})",
            invalid_ts,
            "Todos os timestamps são válidos.",
        )
    )
    order_issue_strs = [
        f"{oi.rel_path} — {oi.description}" for oi in order_issues
    ]
    lines.append(
        _list_section(
            f"Arquivos com ordem incoerente ({len(order_issues)})",
            order_issue_strs,
            "A ordem está coerente com os timestamps.",
        )
    )

    lines += [
        "## Pontos positivos",
        "",
    ]
    for p in positives:
        lines.append(f"- {p}")
    lines.append("")

    lines += [
        "## Sugestões de melhoria",
        "",
    ]
    for s in suggestions:
        lines.append(f"- {s}")
    lines.append("")

    lines += [
        "---",
        "",
        f"_Relatório gerado automaticamente pelo Analisador de Organização de Projetos._",
    ]

    content = "\n".join(lines)

    # ── Salvar arquivo ────────────────────────────────────────────────────────
    reports_dir = _safe_reports_dir()
    filename = f"{project_name}_relatorio.md"
    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(content)

    return filepath

