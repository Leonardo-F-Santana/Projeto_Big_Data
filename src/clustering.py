import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
import plotly.express as px
import plotly.graph_objects as go
from data_processing import carregar_dados, preprocessar_dados


# ===========================================================
# 🚀 RADAR CHART
# ===========================================================
def gerar_radar(df_clustered, titulo):
    numeric_cols = df_clustered.select_dtypes(include=["int", "float"]).columns.tolist()

    # remove "cluster" da lista para não entrar no radar
    if "cluster" in numeric_cols:
        numeric_cols.remove("cluster")

    if len(numeric_cols) < 1:
        print(f"[AVISO] Não há colunas numéricas para gerar radar: {titulo}")
        return None

    medias = df_clustered.groupby("cluster")[numeric_cols].mean()
    categorias = numeric_cols

    fig = go.Figure()

    for cluster_id in medias.index:
        valores = medias.loc[cluster_id].tolist()
        valores += valores[:1]

        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categorias + [categorias[0]],
            fill="toself",
            name=f"Cluster {cluster_id}"
        ))

    fig.update_layout(
        title=titulo,
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )

    fig.show()
    return fig


# ===========================================================
# 🚀 FUNÇÃO GERAL DE CLUSTERIZAÇÃO
# ===========================================================
def gerar_cluster(df, variaveis, k=4, titulo="Cluster"):
    df_cluster = df[variaveis].dropna().copy()
    print(f"\n===== {titulo.upper()} =====")
    print(f"Registros usados: {len(df_cluster)}")
    print("Variáveis:", variaveis)

    numericas = df_cluster.select_dtypes(include=["int", "float"]).columns.tolist()
    categoricas = df_cluster.select_dtypes(include=["object"]).columns.tolist()

    col_trans = ColumnTransformer([
        ("num", StandardScaler(), numericas),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categoricas)
    ])

    pipe = Pipeline([
        ("prep", col_trans),
        ("kmeans", KMeans(n_clusters=k, random_state=42, n_init=10))
    ])

    labels = pipe.fit_predict(df_cluster)
    df_cluster["cluster"] = labels

    print("\nDistribuição dos clusters:")
    print(df_cluster["cluster"].value_counts())

    return df_cluster


# ===========================================================
# 🚀 SCRIPT PRINCIPAL
# ===========================================================
if __name__ == "__main__":
    print(">> Carregando e preparando dados...")

    df = carregar_dados()
    df = preprocessar_dados(df)
    print(f"Total de registros: {len(df)}")

        # =======================================================
    # 1️⃣ CLUSTER RENDA + IDADE — (MELHOR VERSÃO)
    # =======================================================
    vars_renda_idade = ["idade", "salario"]

    cluster_renda = gerar_cluster(
        df,
        variaveis=vars_renda_idade,
        k=4,
        titulo="Cluster Renda + Idade"
    )

    # Criar faixas etárias
    bins_idade = [0, 30, 50, 65, 200]
    labels_idade = ["Jovem (≤30)", "Adulto (31–50)", "Maduro (51–65)", "Idoso (66+)"]
    cluster_renda["faixa_idade"] = pd.cut(cluster_renda["idade"], bins=bins_idade, labels=labels_idade)

    # Criar faixas salariais
    bins_salario = [0, 3000, 6000, 10000, 9999999]
    labels_salario = ["Baixa renda (≤3k)", "Média (3k–6k)", "Alta (6k–10k)", "Muito alta (10k+)"]
    cluster_renda["faixa_salario"] = pd.cut(cluster_renda["salario"], bins=bins_salario, labels=labels_salario)

    # =======================================================
    # A) GRÁFICO: Faixa Etária x Faixa Salarial por Cluster
    # =======================================================

    tabela_faixas = (
        cluster_renda.groupby(["cluster", "faixa_idade", "faixa_salario"])
        .size()
        .reset_index(name="quantidade")
    )

    fig_faixas = px.bar(
        tabela_faixas,
        x="faixa_idade",
        y="quantidade",
        color="faixa_salario",
        facet_col="cluster",
        title="Distribuição por Faixa Etária e Salarial — Cluster Renda + Idade",
        barmode="group",
    )
    fig_faixas.update_layout(xaxis_title="Faixa Etária", yaxis_title="Quantidade")
    fig_faixas.show()

    # =======================================================
    # B) GRÁFICO: Médias (idade média, salário médio, tamanho)
    # =======================================================

    resumo = cluster_renda.groupby("cluster").agg(
        idade_media=("idade", "mean"),
        salario_medio=("salario", "mean"),
        tamanho=("cluster", "count")
    ).reset_index()

    # Barra horizontal das médias
    fig_medias = px.bar(
        resumo,
        x="salario_medio",
        y="cluster",
        orientation="h",
        title="Salário Médio por Cluster",
        labels={"salario_medio": "Salário Médio", "cluster": "Cluster"}
    )
    fig_medias.show()

    fig_medias2 = px.bar(
        resumo,
        x="idade_media",
        y="cluster",
        orientation="h",
        title="Idade Média por Cluster",
        labels={"idade_media": "Idade Média", "cluster": "Cluster"}
    )
    fig_medias2.show()

    fig_tamanho = px.bar(
        resumo,
        x="cluster",
        y="tamanho",
        title="Tamanho de Cada Cluster (Quantidade de Pessoas)",
        labels={"tamanho": "Quantidade", "cluster": "Cluster"}
    )
    fig_tamanho.show()


        # =======================================================
    # 2️⃣ CLUSTER PROFISSIONAL
    # =======================================================
    vars_profissional = ["idade", "salario", "profissao"]

    cluster_prof = gerar_cluster(
        df,
        variaveis=vars_profissional,
        k=4,
        titulo="Cluster Profissional"
    )

    # =======================================================
    # A) Top 10 profissões por cluster (CÓDIGO CORRIGIDO)
    # =======================================================

    # Conta as profissões dentro de cada cluster
    contagem = (
        cluster_prof
        .groupby(["cluster", "profissao"])
        .size()
        .reset_index(name="count")
    )

    # Seleciona top 10 por cluster
    tops = (
        contagem
        .sort_values(["cluster", "count"], ascending=[True, False])
        .groupby("cluster")
        .head(10)
    )

    fig_prof = px.bar(
        tops,
        x="profissao",
        y="count",
        color="cluster",
        title="Top 10 Profissões por Cluster Profissional",
        barmode="group"
    )

    fig_prof.update_layout(xaxis=dict(tickangle=45))
    fig_prof.show()

        # =======================================================
    # B) Gráfico de salário MÉDIO por cluster (mais claro!)
    # =======================================================

    salario_medio = (
        cluster_prof.groupby("cluster")["salario"].mean().reset_index()
    )

    fig_sal_media = px.bar(
        salario_medio,
        x="cluster",
        y="salario",
        title="Salário Médio por Cluster Profissional",
        labels={"cluster": "Cluster", "salario": "Salário Médio (R$)"},
        text_auto=".2f"
    )

    fig_sal_media.update_traces(marker_color="teal")
    fig_sal_media.show()


    # =======================================================
    # C) Radar Chart do cluster profissional
    # =======================================================

    gerar_radar(cluster_prof, "Radar – Cluster Profissional")


    print("\n🏁 Clusterização concluída com sucesso!")
