import unicodedata

import pandas as pd

def merge_df_in_city(df_hosp, df_popul):
    # Normalize text columns for consistent merging
    df_hosp["MUNICIPIO_NORM"] = df_hosp["MUNICIPIO"].apply(normalize_text)
    df_popul["MUNICIPIO_NORM"] = df_popul["NOME DO MUNICÍPIO"].apply(normalize_text)
    
    # Merge hospital and population data on municipality and state
    df_merged = pd.merge(
        df_hosp,
        df_popul,
        left_on=["UF", "MUNICIPIO_NORM"],
        right_on=["UF", "MUNICIPIO_NORM"],
        how="inner"
    )

    return df_merged[[
        "UF",
        "MUNICIPIO_NORM",
        "NOME_ESTABELECIMENTO",
        "DS_TIPO_UNIDADE",
        "NU_TELEFONE",
        "NO_EMAIL",
        "LEITOS_SUS",
        "POPULAÇÃO ESTIMADA"
    ]]
    

def normalize_text(text):
    if pd.isna(text):
        return text

    text = str(text).strip().lower()

    # remove accents
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))

    return text


def hospital_bed_per_capita_in_city(df_hosp, df_popul):
    df_merged = merge_df_in_city(df_hosp, df_popul)

    df_city = df_merged.groupby(["UF", "MUNICIPIO_NORM"]).agg({
        "LEITOS_SUS": "sum",
        "POPULAÇÃO ESTIMADA": "first"
    }).reset_index()


    df_city["LEITOS_TOTAL_PER_THOUSAND"] = (
        df_city["LEITOS_SUS"] / df_city["POPULAÇÃO ESTIMADA"] * 1000
    )

    return df_city.sort_values(
        by="LEITOS_TOTAL_PER_THOUSAND",
        ascending=False
    )

def get_large_cities(df, min_population=100_000, top_n=10, worst=True):
    df_filtered = df[df["POPULAÇÃO ESTIMADA"] > min_population]

    df = (
        df_filtered
        .sort_values("LEITOS_TOTAL_PER_THOUSAND", ascending=worst)
        .head(top_n)
    )

    df["LABEL"] = (
        df["MUNICIPIO_NORM"].str.title() +
        " (" +
        df["POPULAÇÃO ESTIMADA"]
            .astype(int)
            .apply(lambda x: f"{x:,}".replace(",", ".")) +
        " hab)"
    )

    return df
