# app.py (substituir o src/app.py atual)
import streamlit as st
import pandas as pd
from data_processing import carregar_dados, preprocessar_dados
import cluster_module as cm  # import local (arquivo criado)
st.set_page_config(page_title="Dashboard — Projeto Big Data", layout="wide", page_icon="📊")

# ---- Estilo / título
st.title("📊 Dashboard — Projeto Big Data (Azul Tech)")
st.markdown("Painel interativo — EDA & Clusterização")

# ---- Carregar dados
@st.cache_data
def load_data():
    df = carregar_dados()
    df = preprocessar_dados(df)
    return df

df = load_data()

# ---- Sidebar com navegação
st.sidebar.header("Navegação")
page = st.sidebar.radio("Ir para:", ["Visão Geral", "EDA", "Clusters", "Sobre"])

# ---------- PAGE: Visão Geral
if page == "Visão Geral":
    st.header("Visão Geral")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros", f"{len(df):,}")
    col2.metric("Idade média", f"{df['idade'].mean():.1f}")
    col3.metric("Salário médio", f"R$ {df['salario'].mean():,.2f}")
    col4.metric("Profissões únicas", f"{df['profissao'].nunique()}")
    st.markdown("---")
    st.subheader("Amostra dos dados")
    st.dataframe(df.head(200))

# ---------- PAGE: EDA (mantém seus gráficos simples)
elif page == "EDA":
    st.header("Análise Exploratória (EDA)")
    st.subheader("Idade")
    fig_idade = cm.px = None
    fig = None
    fig_idade = (  # histograma
        pd.DataFrame(df["idade"]).dropna()
    )
    fig = None
    st.write("Histograma e gráficos interativos podem ser acessados no arquivo EDA.")

    st.write("Use a aba Clusters para análises por cluster e gráficos detalhados.")

# ---------- PAGE: CLUSTERS
elif page == "Clusters":
    st.header("Clusters")
    st.write("Escolha o tipo de cluster e visualize os gráficos interativos.")

    tipo = st.selectbox("Tipo de Cluster", ["Renda + Idade", "Profissional"])
    k = st.slider("Número de clusters (k)", 2, 6, 4)

    st.markdown("---")
    col_left, col_right = st.columns([2,1])

    if tipo == "Renda + Idade":
        with st.spinner("Gerando cluster Renda + Idade..."):
            df_cluster, resumo, figs = cm.cluster_renda_idade(df, k=k)
        st.subheader("Scatter — Idade x Salário")
        st.plotly_chart(figs["scatter"], width="stretch")
        st.subheader("Salário Médio por Cluster")
        st.plotly_chart(figs["salario_medio_bar"], width="stretch")
        st.subheader("Faixa Etária x Faixa Salarial por Cluster (facets)")
        st.plotly_chart(figs["faixas_facets"], width="stretch")
        st.subheader("Tamanho dos Clusters")
        st.plotly_chart(figs["tamanho_cluster"], width="stretch")
        st.markdown("---")
        st.subheader("Resumo numérico dos clusters")
        st.dataframe(resumo.style.format({"idade_media":"{:.1f}", "salario_medio":"R$ {:,.2f}"}))

    else:
        with st.spinner("Gerando cluster Profissional..."):
            df_cluster, resumo, figs = cm.cluster_profissional(df, k=k)
        st.subheader("Top Profissões por Cluster")
        st.plotly_chart(figs["top_profissoes"], width="stretch")
        st.subheader("Salário Médio por Profissão (bubble por frequência)")
        st.plotly_chart(figs["salario_profissao_scatter"], width="stretch")
        st.subheader("Salário Médio por Cluster")
        st.plotly_chart(figs["salario_medio_cluster"], width="stretch")
        st.markdown("---")
        st.subheader("Resumo numérico dos clusters")
        st.dataframe(resumo.style.format({"idade_media":"{:.1f}", "salario_medio":"R$ {:,.2f}"}))

# ---------- PAGE: Sobre
else:
    st.header("Sobre o Projeto")
    st.markdown("""
    **Projeto:** Análise Exploratório e Clusterização  
    **Autor:** Leonardo Santana  
    **Tecnologias:** Python, Pandas, Plotly, Streamlit, Scikit-Learn  
    **Observações:** Use os controles para ajustar k e explorar.
    """)

