"""
loose_file_checker.py — Identifica arquivos soltos na raiz do projeto.

Um arquivo é considerado "solto" quando está diretamente na raiz da pasta
analisada e existem subpastas presentes — sugerindo que o projeto já tem
alguma estrutura de organização, mas nem todos os arquivos foram alocados.

Se o projeto tem apenas a raiz sem subpastas, todos os arquivos são reportados
como soltos (pois o projeto não tem nenhuma estrutura de pastas).
"""

from typing import List

from .file_scanner import ScanResult


def check_loose_files(scan_result: ScanResult) -> List[str]:
    """
    Retorna a lista de caminhos relativos dos arquivos considerados soltos.

    Critério:
    - Arquivos diretamente na raiz da pasta analisada.
    - A raiz deve ter pelo menos uma subpasta (ou nenhuma — projeto sem estrutura).
    """
    if not scan_result.root_files:
        return []

    # Se existem subpastas, arquivos na raiz são considerados soltos
    # Se não existem subpastas, todos os arquivos estão na raiz — projeto sem estrutura
    return [f.rel_path for f in scan_result.root_files]

