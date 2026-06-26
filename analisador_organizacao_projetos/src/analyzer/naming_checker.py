"""
naming_checker.py — Valida se os nomes dos arquivos seguem o padrão definido:
    ordem_tipo_assunto_aammdd_hhmm.extensao

Exemplos válidos:
    a_prd_login_260522_1150.md
    b_requisitos_cadastro_260523_1850.md

Exemplos inválidos:
    teste.md
    novo.docx
    final2.docx
    b-prd-login-260523-1150.md  (hífen num projeto que usa underscore)
"""

import re
from typing import List, Tuple

from .file_scanner import FileInfo

# Nomes considerados genéricos e pouco descritivos
GENERIC_NAMES = {
    "teste", "test", "novo", "new", "final", "final2", "documento",
    "doc", "arquivo", "file", "temp", "tmp", "copia", "copy",
    "versao_final", "versao_final_agora", "untitled", "semtitulo",
    "rascunho", "draft", "backup", "bkp",
}

# Regex para validar o padrão completo: ordem_tipo_assunto_aammdd_hhmm
# Ex: a_prd_login_260522_1150
FULL_PATTERN_UNDERSCORE = re.compile(
    r'^[a-z]_[a-z][a-z0-9]*(?:_[a-z0-9][a-z0-9]*)+_\d{6}_\d{4}$'
)

FULL_PATTERN_HYPHEN = re.compile(
    r'^[a-z]-[a-z][a-z0-9]*(?:-[a-z0-9][a-z0-9]*)*-\d{6}-\d{4}$'
)


def _stem(filename: str) -> str:
    """Retorna o nome do arquivo sem a extensão."""
    dot_pos = filename.rfind('.')
    if dot_pos > 0:
        return filename[:dot_pos]
    return filename


def _detect_separator(stem: str) -> str:
    """Detecta o separador predominante no nome (underscore, hífen ou espaço)."""
    underscores = stem.count('_')
    hyphens = stem.count('-')
    spaces = stem.count(' ')

    if underscores >= hyphens and underscores >= spaces:
        return '_'
    if hyphens >= underscores and hyphens >= spaces:
        return '-'
    return ' '


def check_naming(
    files: List[FileInfo],
) -> Tuple[List[str], List[str], List[str], str]:
    """
    Verifica os nomes dos arquivos e retorna:
        - invalid_pattern: lista de arquivos fora do padrão
        - generic_names: lista de arquivos com nomes genéricos
        - mixed_separators: lista de arquivos que misturam separadores
        - dominant_separator: separador dominante no projeto ('_', '-' ou ' ')
    """
    invalid_pattern: List[str] = []
    generic: List[str] = []
    mixed: List[str] = []

    # Determinar separador dominante do projeto inteiro
    sep_counts = {'_': 0, '-': 0, ' ': 0}
    for f in files:
        s = _detect_separator(_stem(f.name.lower()))
        sep_counts[s] += 1

    dominant_sep = max(sep_counts, key=lambda k: sep_counts[k])

    for f in files:
        stem = _stem(f.name.lower())

        # 1. Nome genérico?
        if stem in GENERIC_NAMES:
            generic.append(f.rel_path)

        # 2. Separador diferente do dominante?
        file_sep = _detect_separator(stem)
        if file_sep != dominant_sep:
            mixed.append(f.rel_path)

        # 3. Validar padrão completo conforme o separador dominante
        if dominant_sep == '_':
            if not FULL_PATTERN_UNDERSCORE.match(stem):
                invalid_pattern.append(f.rel_path)
        elif dominant_sep == '-':
            if not FULL_PATTERN_HYPHEN.match(stem):
                invalid_pattern.append(f.rel_path)
        else:
            # Espaços: sempre inválido para o padrão
            invalid_pattern.append(f.rel_path)

    return invalid_pattern, generic, mixed, dominant_sep

