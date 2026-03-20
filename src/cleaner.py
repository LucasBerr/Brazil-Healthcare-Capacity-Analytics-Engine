import pandas as pd

REQUIRED_COLUMNS_HOSPITAL = [
    "UF",
    "MUNICIPIO",
    "NOME_ESTABELECIMENTO",
    "DS_TIPO_UNIDADE",
    "NU_TELEFONE",
    "NO_EMAIL",
    "LEITOS_EXISTENTES",
    "LEITOS_SUS"
]
REQUIRED_COLUMNS_POPULATION = [
    "UF",
    "NOME DO MUNICÍPIO",
    "POPULAÇÃO ESTIMADA"
]

def clean_data_hosp(df):
    df = df[REQUIRED_COLUMNS_HOSPITAL].copy()

    numeric_columns_hosp = [
        "LEITOS_SUS"
    ]


    df = coerce_numeric_columns(df, numeric_columns_hosp)
    df = handle_missing_values(df, numeric_columns_hosp)

    return df

def clean_data_popul(df):
    df = df[REQUIRED_COLUMNS_POPULATION].copy()

    numeric_columns_popul = ["POPULAÇÃO ESTIMADA"]

    df = coerce_numeric_columns(df, numeric_columns_popul)
    df = handle_missing_values(df, numeric_columns_popul)
    # Remove empty columns
    df = df.dropna(axis=1, how='all')

    df = df.dropna(axis=0, how='all')

    df = remove_invalid_rows(df)
    return df

def remove_invalid_rows(df):
    VALID_UFS = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO",
    "MA","MT","MS","MG","PA","PB","PR","PE","PI",
    "RJ","RN","RS","RO","RR","SC","SP","SE","TO"
    ]
    df = df[df["UF"].isin(VALID_UFS)]
    return df


def coerce_numeric_columns(df, numeric_columns):
    for col in numeric_columns:
        # Convert to string, replace commas and dots, then convert to numeric
        df[col] =df[col].astype(str).str.replace(",", ".").str.replace(".", "", regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def handle_missing_values(df, numeric_columns):
    df[numeric_columns] = df[numeric_columns].fillna(0)
    return df