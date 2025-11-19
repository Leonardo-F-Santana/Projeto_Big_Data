import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans

# 1) CLUSTER RENDA + IDADE

def cluster_renda_idade(df, k=4, random_state=42):
    
    #Cluster Renda + Idade (numérico).
  
   
    import plotly.express as px

    #remover registros incompletos
    dfc = df.dropna(subset=["idade", "salario"]).copy()

    #matriz numérica
    X = dfc[["idade", "salario"]].astype(float)

    #padronização
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    #KMeans
    km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    labels = km.fit_predict(Xs)
    dfc["cluster"] = labels.astype(int)

    #faixas etárias
    bins_idade = [0, 30, 50, 65, 200]
    labels_idade = ["Jovem (≤30)", "Adulto (31–50)", "Maduro (51–65)", "Idoso (66+)"]
    dfc["faixa_idade"] = pd.cut(dfc["idade"], bins=bins_idade, labels=labels_idade)

    #faixas salariais
    bins_salario = [0, 3000, 6000, 10000, 1e9]
    labels_salario = ["Baixa renda (≤3k)", "Média (3k–6k)", "Alta (6k–10k)", "Muito alta (10k+)"]
    dfc["faixa_salario"] = pd.cut(dfc["salario"], bins=bins_salario, labels=labels_salario)

    #resumo estatístico
    resumo = dfc.groupby("cluster").agg(
        idade_media=("idade", "mean"),
        salario_medio=("salario", "mean"),
        tamanho=("cluster", "count")
    ).reset_index()

    figs = {}

    #Scatter Idade x Salário
    figs["scatter"] = px.scatter(
        dfc,
        x="idade",
        y="salario",
        color="cluster",
        hover_data=["idade", "salario", "faixa_idade", "faixa_salario"],
        title="Cluster Renda x Idade (Scatter)",
        labels={"cluster": "Cluster"}
    )

    #Salário Médio por Cluster
    salario_medio = resumo[["cluster", "salario_medio"]]
    figs["salario_medio_bar"] = px.bar(
        salario_medio,
        x="cluster",
        y="salario_medio",
        title="Salário Médio por Cluster (Renda + Idade)",
        labels={"salario_medio": "Salário Médio (R$)", "cluster": "Cluster"},
        text_auto=".2f"
    )

    #Faixa etária vs faixa salarial
    tabela_faixas = (
        dfc.groupby(["cluster", "faixa_idade", "faixa_salario"])
        .size()
        .reset_index(name="quantidade")
    )

    figs["faixas_facets"] = px.bar(
        tabela_faixas,
        x="faixa_idade",
        y="quantidade",
        color="faixa_salario",
        facet_col="cluster",
        title="Faixa Etária x Faixa Salarial por Cluster",
        barmode="group"
    )

    #Tamanho do cluster
    figs["tamanho_cluster"] = px.bar(
        resumo,
        x="cluster",
        y="tamanho",
        title="Tamanho (quantidade) por Cluster",
        labels={"tamanho": "Quantidade", "cluster": "Cluster"},
        text_auto=True
    )

    return dfc, resumo, figs


def cluster_profissional(df, k=4, random_state=42):
    
    import plotly.express as px
    

    dfc = df.dropna(subset=["idade", "salario", "profissao"]).copy()
    dfc["profissao"] = dfc["profissao"].astype(str)

    numericas = ["idade", "salario"]
    categoricas = ["profissao"]

    #transformação
    col_trans = ColumnTransformer([
        ("num", StandardScaler(), numericas),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categoricas)
    ])

    km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    pipe = Pipeline([("prep", col_trans), ("km", km)])

    # entrada
    X = dfc[numericas + categoricas]
    labels = pipe.fit_predict(X)
    dfc["cluster"] = labels.astype(int)

    #resumo estatístico
    resumo = dfc.groupby("cluster").agg(
        idade_media=("idade", "mean"),
        salario_medio=("salario", "mean"),
        tamanho=("cluster", "count")
    ).reset_index()

    figs = {}

    #Top 10 profissões por cluster
    contagem = (
        dfc.groupby(["cluster", "profissao"])
        .size()
        .reset_index(name="count")
    )

    tops = (
        contagem.sort_values(["cluster", "count"], ascending=[True, False])
        .groupby("cluster")
        .head(10)
    )

    figs["top_profissoes"] = px.bar(
        tops,
        x="count",
        y="profissao",
        color="cluster",
        orientation="h",
        title="Top Profissões por Cluster",
        facet_col="cluster",
        facet_col_wrap=2
    )

    # salário médio por profissão
    media_prof = (
        dfc.groupby(["cluster", "profissao"])["salario"]
        .mean()
        .reset_index()
    )

    freq = (
        dfc.groupby(["cluster", "profissao"]).size()
        .reset_index(name="count")
    )

    merged = pd.merge(media_prof, freq, on=["cluster", "profissao"])

    figs["salario_profissao_scatter"] = px.scatter(
        merged,
        x="salario",
        y="profissao",
        size="count",
        color="cluster",
        title="Salário Médio por Profissão (Bubble Chart)",
        labels={"salario": "Salário Médio (R$)", "profissao": "Profissão"}
    )

    # Salário médio por cluster
    figs["salario_medio_cluster"] = px.bar(
        resumo,
        x="cluster",
        y="salario_medio",
        title="Salário Médio por Cluster (Profissional)",
        labels={"salario_medio": "Salário Médio (R$)"},
        text_auto=".2f"
    )

    return dfc, resumo, figs