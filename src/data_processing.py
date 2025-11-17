import pandas as pd
from datetime import datetime

def carregar_dados():
    df = pd.read_excel('../data/lista2.xls')
    return df

def preprocessar_dados(df):
    
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

   
    if "unnamed:_14" in df.columns:
        df = df.drop(columns=["unnamed:_14"])

    
    df["dt_nasc"] = df["dt_nasc"].astype(str).str.strip()

    
    df["dt_nasc"] = df["dt_nasc"].str.replace(r"\s*\(\d+\)", "", regex=True)

  
    df["dt_nasc"] = pd.to_datetime(df["dt_nasc"], format="%d/%m/%Y", errors="coerce")

    
    hoje = datetime.today()
    df["idade"] = df["dt_nasc"].apply(lambda x: hoje.year - x.year if pd.notnull(x) else None)

    
    df["salario"] = df["salario"].astype(str).str.replace(r"[^0-9,\.]", "", regex=True)
    df["salario"] = df["salario"].str.replace(",", ".")
    df["salario"] = pd.to_numeric(df["salario"], errors="coerce")

    
    df["sexo"] = df["sexo"].astype(str).str.upper().str.strip()
    df["sexo"] = df["sexo"].replace({"F": "Feminino", "M": "Masculino", "RJ": None, "NAN": None})

    df["bairro"] = df["bairro"].astype(str)
    df = df[~df["bairro"].str.contains(r"\d{4}-\d{2}-\d{2}", regex=True)]

    q1 = df["salario"].quantile(0.01)
    q99 = df["salario"].quantile(0.99)
    df = df[df["salario"].between(q1, q99)]

    df = df[df["idade"].between(18, 95, inclusive="both")]

    return df

if __name__ == "__main__":
    df = carregar_dados()
    print("\nAntes do tratamento:", df.shape)
    df = preprocessar_dados(df)
    print("\nDepois do tratamento:", df.shape)
    print("\nColunas finais:", df.columns.tolist())
    print("\nVisualização inicial:\n", df.head())
