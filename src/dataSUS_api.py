from pysus import CNES
from collections import defaultdict
import shutil
from typing import List
import os

GROUP = "LT"

UFS = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO",
    "MA","MT","MS","MG","PA","PB","PR","PE","PI",
    "RJ","RN","RS","RO","RR","SC","SP","SE","TO"
]

MONTH_MAP = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3,
    "Abril": 4, "Maio": 5, "Junho": 6,
    "Julho": 7, "Agosto": 8, "Setembro": 9,
    "Outubro": 10, "Novembro": 11, "Dezembro": 12
}

def download_all_cnes_lt_parquet(year=None, month=None, output_dir="data/parquet/"):
    cnes = CNES()
    cnes.load(GROUP)

    if year is None and month is None:
        year, month = get_updated_year_month(cnes, GROUP)

    destination = build_output_path(output_dir, year, month)

    files = get_cnes_lt_files(cnes, UFS, year, month)

    to_download, cached = split_cached_files(files, destination)

    print(f"[INFO] {len(cached)} já existem")
    print(f"[INFO] {len(to_download)} para download")

    if to_download:
        downloaded = download_files(cnes, to_download)
        move_parquet_files(downloaded, destination)

    return build_final_paths(files, destination)

def get_cnes_lt_files(cnes, ufs, year, month):
    files = cnes.get_files("LT", uf=ufs, year=year, month=month)

    if not files:
        raise ValueError("Nenhum arquivo encontrado")

    return files

def build_output_path(base_dir, year, month):
    path = os.path.join(base_dir, f"{year}_{month:02d}")
    os.makedirs(path, exist_ok=True)
    return path

def split_cached_files(files, destination_dir):
    existing_files = set(os.listdir(destination_dir))

    to_download = []
    cached = []

    for f in files:
        filename = to_parquet_name(f)

        if filename in existing_files:
            cached.append(f)
        else:
            to_download.append(f)

    return to_download, cached

def to_parquet_name(file):
    return os.path.splitext(file.name)[0] + ".parquet"

def download_files(cnes, files):
    if not files:
        return []

    return cnes.download(files)

def build_final_paths(files, destination_dir):
    return [
        os.path.join(destination_dir, to_parquet_name(f))
        for f in files
    ]

def get_updated_year_month(cnes, group):

    files = cnes.get_files(group)

    if not files:
        raise ValueError(f"Nenhum arquivo encontrado no grupo {group}")

    period_count = defaultdict(int)

    for f in files:
        meta = cnes.describe(f)

        # valida campos essenciais
        if "year" not in meta or "month" not in meta:
            continue

        year = int(meta["year"])

        # mês vem como string ("Janeiro", etc)
        month_str = meta["month"]

        month_map = {
            "Janeiro": 1, "Fevereiro": 2, "Março": 3,
            "Abril": 4, "Maio": 5, "Junho": 6,
            "Julho": 7, "Agosto": 8, "Setembro": 9,
            "Outubro": 10, "Novembro": 11, "Dezembro": 12
        }

        month = month_map.get(month_str)

        if month is None:
            continue

        period_count[(year, month)] += 1

    # pega meses completos
    complete_periods = [
        (year, month)
        for (year, month), count in period_count.items()
        if count >= 27
    ]

    if not complete_periods:
        raise ValueError("Nenhum mês completo encontrado")

    latest_year, latest_month = max(complete_periods)

    print(f"[INFO] Último mês completo: {latest_year}-{latest_month:02d}")

    return latest_year, latest_month

def move_parquet_files(file_paths: List[str], destination_dir: str) -> List[str]:
    os.makedirs(destination_dir, exist_ok=True)

    moved_files = []

    for path in file_paths:
        src = str(path)
        filename = os.path.basename(src)
        dst = os.path.join(destination_dir, filename)

        try:
            shutil.move(src, dst)
            moved_files.append(dst)
        except FileNotFoundError:
            print(f"[WARNING] Arquivo não encontrado: {src}")
        except Exception as e:
            print(f"[ERROR] Falha ao mover {src}: {e}")

    print(f"[INFO] {len(moved_files)} arquivos movidos")

    return moved_files