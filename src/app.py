import streamlit as st
import pandas as pd
import plotly.express as px 
from data_processing import carregar_dados, preprocessar_dados
import cluster_module as cm 

st.set_page_config(page_title="Análise Socioeconómica e Clusterização de Perfis Profissionais", layout="wide", page_icon="📊")

#Estilo / título
st.title("📊 Análise Socioeconómica e Clusterização de Perfis Profissionais")
st.markdown("Painel interativo — Análise Exploratória & Clusterização")

#Carrega os dados
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

#Pagina: Visão Geral
if page == "Visão Geral":
    st.header("Visão Geral dos Dados")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Registros", f"{len(df):,}")
    col2.metric("Idade Média", f"{df['idade'].mean():.1f} anos")
    col3.metric("Salário Médio", f"R$ {df['salario'].mean():,.2f}")
    col4.metric("Profissões Distintas", f"{df['profissao'].nunique()}")
    
    st.markdown("---")
    st.subheader(" Amostra dos dados (Primeiras 100 linhas)")
    st.dataframe(df.head(100), use_container_width=True)

#Pagina: EDA (Análise Exploratória Completa)
elif page == "EDA":
    st.header(" Análise Exploratória de Dados (EDA)")
    
    # Cria uma cópia para não alterar o cache original ao criar colunas novas
    df_eda = df.copy()

    #1. Distribuição de Idade ---
    st.subheader("1. Distribuição de Idade")
    fig_idade = px.histogram(
        df_eda, 
        x="idade", 
        nbins=20, 
        title="Frequência por Idade",
        color_discrete_sequence=["#3366CC"]
    )
    fig_idade.update_layout(bargap=0.1)
    st.plotly_chart(fig_idade, use_container_width=True)

    st.markdown("---")

    #2. Distribuição por Faixa Salarial ---
    st.subheader("2. Distribuição por Faixa Salarial")
    
    # Criando faixas (Logica trazida do eda.py)
    faixas = [0, 1500, 3000, 5000, 8000, 12000, df_eda["salario"].max()]
    faixas_nomes = ["Até 1.500", "1.501 – 3.000", "3.001 – 5.000", "5.001 – 8.000", "8.001 – 12.000", "Acima de 12.000"]
    
    try:
        df_eda["faixa_salarial"] = pd.cut(df_eda["salario"], bins=faixas, labels=faixas_nomes, include_lowest=True)
        
        faixa_freq = df_eda["faixa_salarial"].value_counts().sort_index().reset_index()
        faixa_freq.columns = ["faixa_salarial", "quantidade"]

        fig_salario = px.bar(
            faixa_freq,
            x="quantidade",
            y="faixa_salarial",
            orientation="h",
            text="quantidade",
            title="Quantidade de Pessoas por Faixa Salarial",
            color="quantidade",
            color_continuous_scale="Blues"
        )
        fig_salario.update_layout(yaxis=dict(categoryorder='array', categoryarray=faixas_nomes))
        st.plotly_chart(fig_salario, use_container_width=True)
    except Exception as e:
        st.warning(f"Não foi possível gerar gráfico de faixas salariais: {e}")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    #3. Distribuição por Sexo ---
    with col_a:
        st.subheader("3. Distribuição por Sexo")
        sexo_freq = df_eda["sexo"].value_counts(dropna=False).reset_index()
        sexo_freq.columns = ["sexo", "quantidade"]
        sexo_freq["percentual"] = (sexo_freq["quantidade"] / len(df_eda) * 100).round(2)

        fig_sexo = px.bar(
            sexo_freq,
            x="quantidade",
            y="sexo",
            orientation="h",
            text="percentual",
            title="Divisão por Gênero (%)",
            color="sexo",
            color_discrete_map={
                "Masculino": "#1f77b4",
                "Feminino": "#ff69b4",
                "NA": "#808080"
            }
        )
        fig_sexo.update_traces(texttemplate="%{text}%")
        st.plotly_chart(fig_sexo, use_container_width=True)

    #4. Top 10 Cidades ---
    with col_b:
        st.subheader("4. Top 10 Cidades")
        if "cidade" in df_eda.columns:
            df_cid = df_eda.dropna(subset=["cidade"]).copy()
            df_cid["cidade"] = df_cid["cidade"].str.title()
            cid_top10 = df_cid["cidade"].value_counts().reset_index().head(10)
            cid_top10.columns = ["cidade", "quantidade"]
            cid_top10 = cid_top10.sort_values(by="quantidade", ascending=True) # Para o gráfico ficar na ordem certa

            fig_cid = px.bar(
                cid_top10,
                x="quantidade",
                y="cidade",
                orientation="h",
                text="quantidade",
                title="Cidades com Mais Registros",
                color="quantidade",
                color_continuous_scale="Teal"
            )
            st.plotly_chart(fig_cid, use_container_width=True)
        else:
            st.write("Coluna 'cidade' não encontrada.")

    st.markdown("---")

    #Top 10 Profissões + Salário ---
    st.subheader("5. Top 10 Profissões e Salário Mediano")
    if "profissao" in df_eda.columns:
        df_prof = df_eda.dropna(subset=["profissao"]).copy()
        df_prof["profissao"] = df_prof["profissao"].str.title()

        # Contagem
        prof_freq = df_prof["profissao"].value_counts().reset_index()
        prof_freq.columns = ["profissao", "quantidade"]
        
        # Mediana Salarial
        salary_median = df_prof.groupby("profissao")["salario"].median().reset_index()
        salary_median.columns = ["profissao", "salario_mediano"]

        # Merge
        prof_final = pd.merge(prof_freq, salary_median, on="profissao")
        prof_top10 = prof_final.head(10).sort_values(by="quantidade", ascending=True)

        # Texto customizado no gráfico
        prof_top10["label"] = (
            prof_top10["quantidade"].astype(str) + " pessoas | Mediana: R$ " + 
            prof_top10["salario_mediano"].round(2).astype(str)
        )

        fig_prof = px.bar(
            prof_top10,
            x="quantidade",
            y="profissao",
            orientation="h",
            text="label",
            title="Profissões Mais Comuns x Salário",
            color="quantidade",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_prof, use_container_width=True)

# Pagina: CLUSTERS
elif page == "Clusters":
    st.header("Análise de Clusters (K-Means)")
    st.write("Use os controles abaixo para segmentar a base de dados.")

    col_sel1, col_sel2 = st.columns([1, 1])
    with col_sel1:
        tipo = st.selectbox("Selecione o Modelo de Cluster", ["Renda + Idade", "Profissional"])
    with col_sel2:
        k = st.slider("Número de Grupos (K)", 2, 6, 4)

    st.markdown("---")
    
    if tipo == "Renda + Idade":
        with st.spinner(f"Processando clusterização com K={k}..."):
            
            df_cluster, resumo, figs = cm.cluster_renda_idade(df, k=k)
        
        # Layout dos Gráficos
        st.subheader("Dispersão: Idade vs. Salário")
        st.plotly_chart(figs["scatter"], use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Salário Médio por Grupo")
            st.plotly_chart(figs["salario_medio_bar"], use_container_width=True)
        with c2:
            st.subheader("Tamanho dos Grupos")
            st.plotly_chart(figs["tamanho_cluster"], use_container_width=True)
            
        st.subheader("Distribuição: Faixa Etária x Faixa Salarial")
        st.plotly_chart(figs["faixas_facets"], use_container_width=True)
        
        st.markdown("### Resumo Estatístico")
        st.dataframe(resumo.style.format({"idade_media":"{:.1f} anos", "salario_medio":"R$ {:,.2f}"}), use_container_width=True)

    else:
        with st.spinner(f"Processando clusterização Profissional com K={k}..."):
            df_cluster, resumo, figs = cm.cluster_profissional(df, k=k)
            
        st.subheader("🏆 Top Profissões por Cluster")
        st.plotly_chart(figs["top_profissoes"], use_container_width=True)
        
        st.subheader("💼 Salário Médio por Profissão (Tamanho = Frequência)")
        st.plotly_chart(figs["salario_profissao_scatter"], use_container_width=True)
        
        st.subheader("💰 Salário Médio Global do Cluster")
        st.plotly_chart(figs["salario_medio_cluster"], use_container_width=True)
        
        st.markdown("###Resumo Estatístico")
        st.dataframe(resumo.style.format({"idade_media":"{:.1f} anos", "salario_medio":"R$ {:,.2f}"}), use_container_width=True)

#Pagina:Sobre
else:
    st.header("Sobre o Projeto")
    st.markdown("""
    ### 📘 Projeto Big Data
    Este dashboard foi desenvolvido para facilitar a visualização de dados demográficos e profissionais, 
    utilizando técnicas de **Análise Exploratória (EDA)** e **Machine Learning (Clusterização)**.

    **Funcionalidades:**
    - **Visão Geral:** Métricas rápidas da base.
    - **EDA:** Gráficos detalhados de idade, salário, sexo e geografia.
    - **Clusters:** Segmentação automática de perfis usando o algoritmo K-Means.

    **Tecnologias:**
    - Python
    - Streamlit
    - Plotly Express
    - Scikit-Learn (K-Means)
    - Pandas
    """)