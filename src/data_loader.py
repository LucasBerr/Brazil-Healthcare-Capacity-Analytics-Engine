import pandas as pd

def load_data(path, skip_rows=0, encod="latin-1"):
    df = pd.read_csv(
        path,
        sep=";",
        encoding=encod,
        skiprows=skip_rows
    )

    # Remove leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()

    return df

def validate_data_hosp(df):
    required_columns = [
    "UF",
    "MUNICIPIO",
    "NOME_ESTABELECIMENTO",
    "DS_TIPO_UNIDADE",
    "NU_TELEFONE",
    "NO_EMAIL",
    "LEITOS_SUS",
    ]
    validate_columns(df, required_columns)

def validate_data_popul(df):
    required_columns = [
        "UF",
        "NOME DO MUNICÍPIO",
        "POPULAÇÃO ESTIMADA"
    ]
    validate_columns(df, required_columns)

def validate_types(df):
    pass


def validate_columns(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")
    

    

