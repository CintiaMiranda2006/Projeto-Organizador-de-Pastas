"""
timestamp_checker.py — Valida se o timestamp existe nos nomes dos arquivos e se
está no formato correto: AAMMDD_HHMM

Exemplos válidos:
    260622_1850  →  ano=26, mês=06, dia=22, hora=18, min=50
    260101_0000

Exemplos inválidos:
    991399_2500  →  mês=13, hora=25
    260622       →  sem horário
"""

import re
from dataclasses import dataclass
from typing import List, Tuple

from .file_scanner import FileInfo

# Regex para encontrar o padrão AAMMDD_HHMM em qualquer posição no stem
TIMESTAMP_RE = re.compile(r'(\d{6})_(\d{4})')


@dataclass
class TimestampResult:
    rel_path: str
    has_timestamp: bool
    date_str: str = ""    # AAMMDD
    time_str: str = ""    # HHMM
    is_valid: bool = False
    error: str = ""


def _validate_date_time(date_str: str, time_str: str) -> Tuple[bool, str]:
    """
    Valida se AAMMDD e HHMM têm valores coerentes.
    Retorna (is_valid, mensagem_de_erro).
    """
    try:
        # Ano: qualquer valor de 00-99 é aceito (representação de 2 dígitos)
        month = int(date_str[2:4])
        day = int(date_str[4:6])
        hour = int(time_str[0:2])
        minute = int(time_str[2:4])
    except (ValueError, IndexError):
        return False, "Timestamp com dígitos inválidos."

    if not 1 <= month <= 12:
        return False, f"Mês inválido: {month:02d} (deve ser 01–12)."
    if not 1 <= day <= 31:
        return False, f"Dia inválido: {day:02d} (deve ser 01–31)."
    if not 0 <= hour <= 23:
        return False, f"Hora inválida: {hour:02d} (deve ser 00–23)."
    if not 0 <= minute <= 59:
        return False, f"Minuto inválido: {minute:02d} (deve ser 00–59)."

    return True, ""


def _stem(filename: str) -> str:
    """Retorna o nome do arquivo sem a extensão."""
    dot_pos = filename.rfind('.')
    if dot_pos > 0:
        return filename[:dot_pos]
    return filename


def check_timestamps(files: List[FileInfo]) -> List[TimestampResult]:
    """
    Para cada arquivo, verifica:
    - Se existe um timestamp no padrão AAMMDD_HHMM.
    - Se o timestamp está no final do stem (antes da extensão).
    - Se os valores do timestamp são válidos.

    Retorna uma lista de TimestampResult com o status de cada arquivo.
    """
    results: List[TimestampResult] = []

    for f in files:
        stem = _stem(f.name.lower())
        match = TIMESTAMP_RE.search(stem)

        if not match:
            results.append(TimestampResult(
                rel_path=f.rel_path,
                has_timestamp=False,
                error="Timestamp ausente.",
            ))
            continue

        date_str = match.group(1)
        time_str = match.group(2)

        # Verificar se o timestamp está ao final do stem
        expected_suffix = f"{date_str}_{time_str}"
        is_at_end = stem.endswith(expected_suffix)

        if not is_at_end:
            results.append(TimestampResult(
                rel_path=f.rel_path,
                has_timestamp=True,
                date_str=date_str,
                time_str=time_str,
                is_valid=False,
                error="Timestamp não está no final do nome (antes da extensão).",
            ))
            continue

        is_valid, error_msg = _validate_date_time(date_str, time_str)

        results.append(TimestampResult(
            rel_path=f.rel_path,
            has_timestamp=True,
            date_str=date_str,
            time_str=time_str,
            is_valid=is_valid,
            error=error_msg,
        ))

    return results

