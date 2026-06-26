"""
order_checker.py — Verifica se a letra de ordem (a, b, c…) está coerente com
o timestamp dos arquivos dentro de cada diretório.

Regra:
    - 'a' representa o arquivo mais antigo.
    - 'b' deve ter timestamp maior que 'a'.
    - 'c' deve ter timestamp maior que 'b'.
    - Se a ordenação alfabética das letras não corresponder à cronológica dos
      timestamps, o sistema aponta inconsistência.

Exemplo de problema:
    a_prd_login_260523_1150.md    → timestamp: 260523_1150
    b_prd_cadastro_260522_1850.md → timestamp: 260522_1850  ← mais antigo que 'a'!
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional

from .file_scanner import FileInfo
from .timestamp_checker import TIMESTAMP_RE

# Regex para capturar a letra de ordem no início do stem
ORDER_LETTER_RE = re.compile(r'^([a-z])(?:[_\-])')


@dataclass
class OrderIssue:
    rel_path: str
    order_letter: str
    timestamp: str
    expected_after: str   # qual arquivo deveria ser anterior
    description: str


def _extract_timestamp_value(filename: str) -> Optional[str]:
    """
    Extrai o timestamp do nome do arquivo para comparação lexicográfica.
    Retorna 'AAMMDD_HHMM' como string (comparação lexicográfica funciona
    corretamente nesse formato).
    """
    stem = filename.lower()
    dot = stem.rfind('.')
    if dot > 0:
        stem = stem[:dot]

    match = TIMESTAMP_RE.search(stem)
    if match:
        return f"{match.group(1)}_{match.group(2)}"
    return None


def _extract_order_letter(filename: str) -> Optional[str]:
    """Extrai a letra de ordem do início do nome do arquivo (ex: 'a', 'b', 'c')."""
    match = ORDER_LETTER_RE.match(filename.lower())
    if match:
        return match.group(1)
    return None


def check_order(files: List[FileInfo]) -> List[OrderIssue]:
    """
    Agrupa arquivos por diretório e verifica se a letra de ordem está coerente
    com o timestamp dentro de cada grupo.

    Retorna uma lista de OrderIssue para cada arquivo com ordem incoerente.
    """
    # Agrupar arquivos por pasta pai
    by_dir: Dict[str, List[FileInfo]] = defaultdict(list)
    for f in files:
        by_dir[f.parent_dir].append(f)

    issues: List[OrderIssue] = []

    for dir_path, dir_files in by_dir.items():
        # Filtrar apenas arquivos que têm letra de ordem E timestamp
        ordered_files = []
        for f in dir_files:
            letter = _extract_order_letter(f.name)
            ts = _extract_timestamp_value(f.name)
            if letter is not None and ts is not None:
                ordered_files.append((letter, ts, f))

        if len(ordered_files) < 2:
            # Não é possível verificar coerência com menos de 2 arquivos
            continue

        # Ordenar pela letra de ordem (ordem alfabética = ordem esperada)
        ordered_by_letter = sorted(ordered_files, key=lambda x: x[0])

        # Verificar se os timestamps crescem junto com as letras
        for i in range(1, len(ordered_by_letter)):
            prev_letter, prev_ts, prev_file = ordered_by_letter[i - 1]
            curr_letter, curr_ts, curr_file = ordered_by_letter[i]

            if curr_ts <= prev_ts:
                issues.append(OrderIssue(
                    rel_path=curr_file.rel_path,
                    order_letter=curr_letter,
                    timestamp=curr_ts,
                    expected_after=prev_file.rel_path,
                    description=(
                        f"'{curr_letter}' ({curr_ts}) deveria ter timestamp "
                        f"maior que '{prev_letter}' ({prev_ts}), "
                        f"mas está igual ou anterior."
                    ),
                ))

    return issues

