"""
empty_checker.py — Identifica arquivos vazios (tamanho zero) e pastas vazias
(sem nenhum arquivo, nem mesmo em subpastas).
"""

from typing import List, Tuple

from .file_scanner import DirInfo, FileInfo, ScanResult


def check_empty_files(files: List[FileInfo]) -> List[str]:
    """
    Retorna a lista de caminhos relativos dos arquivos com tamanho zero.
    """
    return [f.rel_path for f in files if f.size == 0]


def check_empty_dirs(scan_result: ScanResult) -> List[str]:
    """
    Retorna a lista de caminhos relativos das pastas que não contêm nenhum
    arquivo em toda a sua subárvore.

    Uma pasta é considerada vazia se não existir nenhum arquivo sob ela
    (recursivo), não apenas no nível direto.
    """
    import os

    empty_dirs: List[str] = []

    for d in scan_result.dirs:
        # Verificar se existe algum arquivo com caminho que começa com d.path
        has_file = any(
            f.path.startswith(d.path + os.sep) or f.path == d.path
            for f in scan_result.files
        )
        if not has_file:
            empty_dirs.append(d.rel_path)

    # Remover subpastas de pastas já marcadas como vazias para evitar duplicidade
    # (se a pasta pai já está vazia, as subpastas estão implicitamente inclusas)
    cleaned: List[str] = []
    for d_path in sorted(empty_dirs):
        is_child_of_existing = any(
            d_path.startswith(existing + os.sep)
            for existing in cleaned
        )
        if not is_child_of_existing:
            cleaned.append(d_path)

    return cleaned

