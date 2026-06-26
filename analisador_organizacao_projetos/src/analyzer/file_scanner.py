"""
file_scanner.py — Percorre a estrutura do projeto e retorna informações sobre
arquivos e pastas: caminhos, tamanhos, extensões e hierarquia.
"""

import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class FileInfo:
    """Informações sobre um arquivo encontrado."""
    name: str
    path: str          # caminho absoluto
    rel_path: str      # caminho relativo à raiz analisada
    extension: str
    size: int          # tamanho em bytes
    parent_dir: str    # caminho absoluto da pasta pai


@dataclass
class DirInfo:
    """Informações sobre um diretório encontrado."""
    name: str
    path: str          # caminho absoluto
    rel_path: str      # caminho relativo à raiz analisada
    file_count: int    # quantidade de arquivos diretos (não recursivo)


@dataclass
class ScanResult:
    """Resultado completo do escaneamento."""
    root_path: str
    root_name: str
    files: List[FileInfo] = field(default_factory=list)
    dirs: List[DirInfo] = field(default_factory=list)
    root_files: List[FileInfo] = field(default_factory=list)   # arquivos direto na raiz


def scan(folder_path: str) -> ScanResult:
    """
    Percorre recursivamente a pasta fornecida e retorna um ScanResult com
    todos os arquivos e diretórios encontrados.
    """
    folder_path = os.path.abspath(folder_path)

    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"O caminho '{folder_path}' não é uma pasta válida.")

    root_name = os.path.basename(folder_path)
    result = ScanResult(root_path=folder_path, root_name=root_name)

    for dirpath, dirnames, filenames in os.walk(folder_path):
        # Ordenar para garantir processamento consistente
        dirnames.sort()
        filenames.sort()

        rel_dir = os.path.relpath(dirpath, folder_path)

        # Registrar cada subdiretório encontrado (exceto a raiz em si)
        for dname in dirnames:
            abs_dpath = os.path.join(dirpath, dname)
            rel_dpath = os.path.relpath(abs_dpath, folder_path)

            # Conta apenas arquivos diretos nesta pasta (não recursivo)
            try:
                direct_files = [
                    f for f in os.listdir(abs_dpath)
                    if os.path.isfile(os.path.join(abs_dpath, f))
                ]
            except PermissionError:
                direct_files = []

            result.dirs.append(DirInfo(
                name=dname,
                path=abs_dpath,
                rel_path=rel_dpath,
                file_count=len(direct_files),
            ))

        # Registrar cada arquivo encontrado
        for fname in filenames:
            abs_fpath = os.path.join(dirpath, fname)
            rel_fpath = os.path.relpath(abs_fpath, folder_path)
            _, ext = os.path.splitext(fname)

            try:
                size = os.path.getsize(abs_fpath)
            except OSError:
                size = 0

            finfo = FileInfo(
                name=fname,
                path=abs_fpath,
                rel_path=rel_fpath,
                extension=ext.lower(),
                size=size,
                parent_dir=dirpath,
            )
            result.files.append(finfo)

            # Arquivo está diretamente na raiz?
            if dirpath == folder_path:
                result.root_files.append(finfo)

    return result
