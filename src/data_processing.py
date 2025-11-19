import pandas as pd
import os
from datetime import datetime

def carregar_dados():
    
    caminhos_possiveis = [
        '../data/lista2.xls',
        'data/lista2.xls',
        'lista2.xls',
        '../data/lista2.xlsx', # Caso seja xlsx
        'data/lista2.xlsx'
    ]
    
    df = None
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            print(f"Arquivo encontrado em: {caminho}")
            try:
                df = pd.read_excel(caminho)
            except Exception as e:
                print(f"Erro ao ler Excel, tentando CSV ou outra engine: {e}")
                continue
            break
    
    if df is None:
        raise FileNotFoundError("O arquivo de dados (lista2.xls ou .xlsx) não foi encontrado nas pastas data/ ou ../data/")

    return df

def preprocessar_dados(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    if "unnamed:_14" in df.columns:
        df = df.drop(columns=["unnamed:_14"])

    # Tratamento de data
    df["dt_nasc"] = df["dt_nasc"].astype(str).str.strip()
    df["dt_nasc"] = df["dt_nasc"].str.replace(r"\s*\(\d+\)", "", regex=True)
    df["dt_nasc"] = pd.to_datetime(df["dt_nasc"], format="%d/%m/%Y", errors="coerce")

    # Idade
    hoje = datetime.today()
    df["idade"] = df["dt_nasc"].apply(lambda x: hoje.year - x.year if pd.notnull(x) else None)

    # Salário
    df["salario"] = df["salario"].astype(str).str.replace(r"[^0-9,\.]", "", regex=True)
    # Se o formato for brasileiro (1.000,00), remove ponto de milhar e troca virgula por ponto
    if df["salario"].str.contains(",").any():
        df["salario"] = df["salario"].str.replace(".", "", regex=False) 
        df["salario"] = df["salario"].str.replace(",", ".", regex=False)
        
    df["salario"] = pd.to_numeric(df["salario"], errors="coerce")

    # Sexo
    df["sexo"] = df["sexo"].astype(str).str.upper().str.strip()
    df["sexo"] = df["sexo"].replace({"F": "Feminino", "M": "Masculino", "RJ": None, "NAN": None})

    # Bairro
    df["bairro"] = df["bairro"].astype(str)
    df = df[~df["bairro"].str.contains(r"\d{4}-\d{2}-\d{2}", regex=True)]

    # Filtros de outliers e idade
    if not df["salario"].isnull().all():
        q1 = df["salario"].quantile(0.01)
        q99 = df["salario"].quantile(0.99)
        df = df[df["salario"].between(q1, q99)]

    df = df[df["idade"].between(18, 95, inclusive="both")]

    return df