"""
analyzer.py — Arquivo principal do Analisador de Organização de Projetos.

Coordena o fluxo completo de análise:
    1. Ler pasta de projeto
    2. Mapear arquivos e diretórios
    3. Validar arquivos soltos
    4. Validar arquivos vazios
    5. Validar pastas vazias
    6. Validar padrão de nomes
    7. Validar timestamps
    8. Validar coerência de ordem
    9. Calcular nota
   10. Gerar relatório Markdown

Uso:
    python src/analyzer.py <caminho_da_pasta>

Exemplos:
    python src/analyzer.py ./samples/projeto_organizado
    python src/analyzer.py ./samples/projeto_baguncado
    python src/analyzer.py C:/Users/user/meu_projeto
"""

import sys
import os

# Garante que os módulos do pacote src/ são importados corretamente mesmo
# quando o script é executado de fora da pasta src/
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from file_scanner import scan
from naming_checker import check_naming
from timestamp_checker import check_timestamps
from order_checker import check_order
from empty_checker import check_empty_files, check_empty_dirs
from loose_file_checker import check_loose_files
from score import calculate_score
from report import generate_report


def _print_separator(char: str = "─", width: int = 60) -> None:
    print(char * width)


def analyze(folder_path: str) -> None:
    """
    Executa a análise completa da pasta fornecida e gera o relatório.
    """
    _print_separator("═")
    print("  Analisador de Organização de Projetos")
    _print_separator("═")
    print(f"  Pasta: {os.path.abspath(folder_path)}")
    _print_separator()

    # ── 1. Escanear pasta ─────────────────────────────────────────────────────
    print("⏳ Lendo estrutura da pasta...")
    try:
        scan_result = scan(folder_path)
    except NotADirectoryError as exc:
        print(f"\n❌ Erro: {exc}")
        sys.exit(1)

    print(f"   {len(scan_result.files)} arquivo(s) | {len(scan_result.dirs)} pasta(s)")

    # ── 2. Arquivos soltos ────────────────────────────────────────────────────
    print("⏳ Verificando arquivos soltos...")
    loose_files = check_loose_files(scan_result)

    # ── 3. Arquivos e pastas vazias ───────────────────────────────────────────
    print("⏳ Verificando arquivos e pastas vazios...")
    empty_files = check_empty_files(scan_result.files)
    empty_dirs = check_empty_dirs(scan_result)

    # ── 4. Padrão de nomes ────────────────────────────────────────────────────
    print("⏳ Validando padrão de nomes...")
    invalid_pattern, generic_names, mixed_separators, dominant_sep = check_naming(
        scan_result.files
    )

    # ── 5. Timestamps ─────────────────────────────────────────────────────────
    print("⏳ Validando timestamps...")
    timestamp_results = check_timestamps(scan_result.files)

    # ── 6. Coerência de ordem ─────────────────────────────────────────────────
    print("⏳ Verificando coerência de ordem...")
    order_issues = check_order(scan_result.files)

    # ── 7. Nota final ─────────────────────────────────────────────────────────
    print("⏳ Calculando nota...")
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

    # ── 8. Relatório ──────────────────────────────────────────────────────────
    print("⏳ Gerando relatório...")
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

    # ── Resultado no terminal ─────────────────────────────────────────────────
    _print_separator()
    print(f"\n  Projeto analisado: {scan_result.root_name}")
    print(f"\n  Nota final: {score.total}/10\n")

    # Mostrar problemas encontrados
    missing_ts_count = sum(1 for r in timestamp_results if not r.has_timestamp)
    invalid_ts_count = sum(1 for r in timestamp_results if r.has_timestamp and not r.is_valid)

    issues = []
    if loose_files:
        issues.append(f"  • {len(loose_files)} arquivo(s) solto(s) na raiz.")
    if empty_files:
        issues.append(f"  • {len(empty_files)} arquivo(s) vazio(s).")
    if empty_dirs:
        issues.append(f"  • {len(empty_dirs)} pasta(s) vazia(s).")
    if invalid_pattern:
        issues.append(f"  • {len(invalid_pattern)} arquivo(s) fora do padrão de nome.")
    if generic_names:
        issues.append(f"  • {len(generic_names)} arquivo(s) com nome genérico.")
    if mixed_separators:
        issues.append(f"  • {len(mixed_separators)} arquivo(s) com separador inconsistente.")
    if missing_ts_count:
        issues.append(f"  • {missing_ts_count} arquivo(s) sem timestamp.")
    if invalid_ts_count:
        issues.append(f"  • {invalid_ts_count} arquivo(s) com timestamp inválido.")
    if order_issues:
        issues.append(f"  • {len(order_issues)} arquivo(s) com ordem incoerente.")

    if issues:
        print("  Problemas encontrados:")
        for issue in issues:
            print(issue)
    else:
        print("  ✅ Nenhum problema encontrado. Projeto bem organizado!")

    print()
    _print_separator()
    print(f"\n  ✅ Análise concluída.")
    print(f"  📄 Relatório gerado em: {report_path}")
    print()


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python src/analyzer.py <caminho_da_pasta>")
        print()
        print("Exemplos:")
        print("  python src/analyzer.py ./samples/projeto_organizado")
        print("  python src/analyzer.py ./samples/projeto_baguncado")
        print("  python src/analyzer.py C:/Users/usuario/meu_projeto")
        sys.exit(1)

    folder_path = sys.argv[1]
    analyze(folder_path)


if __name__ == "__main__":
    main()
