import pandas as pd
from pathlib import Path
from analyzer import uti_per_capita_in_city
from data_loader import load_data, validate_data_hosp, validate_data_popul
from cleaner import clean_data_hosp, clean_data_popul


def main():

    BASE_DIR = Path(__file__).resolve().parent.parent
    data_path_hosp = BASE_DIR / "data" / "Leitos_2026.csv"
    data_path_popul = BASE_DIR / "data" / "POP2025_20251031(Municípios).csv"
    
    df_hosp = load_data(data_path_hosp)
    df_popul = load_data(data_path_popul, skip_rows = 1, encod="utf-8")

    validate_data_popul(df_popul)
    validate_data_hosp(df_hosp)
    df_hosp = clean_data_hosp(df_hosp)
    df_popul = clean_data_popul(df_popul)

    df_uit_per_capita_in_city = uti_per_capita_in_city(df_hosp, df_popul)

    print(df_popul)
    print(df_hosp)
    print(df_uit_per_capita_in_city)
    





if __name__ == "__main__":
    main()