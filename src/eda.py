import streamlit as st
import pandas as pd
import plotly.express as px 
from data_processing import carregar_dados, preprocessar_dados
import cluster_module as cm 

st.set_page_config(page_title="Dashboard — Projeto Big Data", layout="wide", page_icon="📊")

#Estilo / título
st.title("📊 Dashboard — Projeto Big Data")
st.markdown("Painel interativo — EDA & Clusterização")

# Carregar dados
@st.cache_data
def load_data():
    try:
        df = carregar_dados()
        df = preprocessar_dados(df)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

#Sidebar com navegação
st.sidebar.header("Navegação")
page = st.sidebar.radio("Ir para:", ["Visão Geral", "EDA", "Clusters", "Sobre"])

#Pagina: Visão Geral(resumão)
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

#Pagina: EDA
elif page == "EDA":
    st.header("Análise Exploratória (EDA)")
    
    # Visualização rápida para o Dashboard
    st.subheader("Distribuição de Idade")
    fig_idade = px.histogram(df, x="idade", nbins=20, title="Histograma de Idades")
    st.plotly_chart(fig_idade, use_container_width=True)

    st.subheader("Distribuição Salarial")
    fig_salario = px.histogram(df, x="salario", nbins=30, title="Histograma de Salários")
    st.plotly_chart(fig_salario, use_container_width=True)

    st.markdown("---")
    st.info("Para ver a análise exploratória completa e detalhada (printada no console), execute o arquivo `src/eda.py` separadamente.")

#Pagina: CLUSTERS
elif page == "Clusters":
    st.header("Clusters")
    st.write("Escolha o tipo de cluster e visualize os gráficos interativos.")

    tipo = st.selectbox("Tipo de Cluster", ["Renda + Idade", "Profissional"])
    k = st.slider("Número de clusters (k)", 2, 6, 4)

    st.markdown("---")
    
    if tipo == "Renda + Idade":
        with st.spinner("Gerando cluster Renda + Idade..."):
            df_cluster, resumo, figs = cm.cluster_renda_idade(df, k=k)
        
        st.subheader("Scatter — Idade x Salário")
        st.plotly_chart(figs["scatter"], use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Salário Médio por Cluster")
            st.plotly_chart(figs["salario_medio_bar"], use_container_width=True)
        with c2:
            st.subheader("Tamanho dos Clusters")
            st.plotly_chart(figs["tamanho_cluster"], use_container_width=True)
            
        st.subheader("Faixa Etária x Faixa Salarial por Cluster")
        st.plotly_chart(figs["faixas_facets"], use_container_width=True)
        
        st.markdown("---")
        st.subheader("Resumo numérico")
        st.dataframe(resumo.style.format({"idade_media":"{:.1f}", "salario_medio":"R$ {:,.2f}"}))

    else:
        with st.spinner("Gerando cluster Profissional..."):
            df_cluster, resumo, figs = cm.cluster_profissional(df, k=k)
            
        st.subheader("Top Profissões por Cluster")
        st.plotly_chart(figs["top_profissoes"], use_container_width=True)
        
        st.subheader("Salário Médio por Profissão")
        st.plotly_chart(figs["salario_profissao_scatter"], use_container_width=True)
        
        st.subheader("Salário Médio por Cluster")
        st.plotly_chart(figs["salario_medio_cluster"], use_container_width=True)
        
        st.markdown("---")
        st.subheader("Resumo numérico")
        st.dataframe(resumo.style.format({"idade_media":"{:.1f}", "salario_medio":"R$ {:,.2f}"}))

#Pagina: Sobre
else:
    st.header("Sobre o Projeto")
    st.markdown("""
    **Projeto:** Análise Exploratória e Clusterização  
    **Autor:** Leonardo Santana  
    **Tecnologias:** Python, Pandas, Plotly, Streamlit, Scikit-Learn
    """)