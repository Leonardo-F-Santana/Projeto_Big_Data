import pandas as pd
import plotly.express as px
from data_processing import carregar_dados, preprocessar_dados

df = carregar_dados()
df = preprocessar_dados(df)

print("Total de registros após limpeza:", len(df))


fig_idade = px.histogram(
    df,
    x="idade",
    nbins=20,
    title="Distribuição de Idade"
)
fig_idade.show()


faixas = [0, 1500, 3000, 5000, 8000, 12000, df["salario"].max()]
faixas_nomes = ["Até 1.500", "1.501 – 3.000", "3.001 – 5.000", "5.001 – 8.000", "8.001 – 12.000", "Acima de 12.000"]
df["faixa_salarial"] = pd.cut(df["salario"], bins=faixas, labels=faixas_nomes, include_lowest=True)

faixa_freq = df["faixa_salarial"].value_counts().sort_index()
faixa_freq = faixa_freq.reset_index()
faixa_freq.columns = ["faixa_salarial", "quantidade"]

fig_salario = px.bar(
    faixa_freq,
    x="quantidade",
    y="faixa_salarial",
    orientation="h",
    text="quantidade",
    title="Distribuição por Faixa Salarial",
    color="quantidade",
    color_continuous_scale="Blues"
)
fig_salario.update_layout(yaxis=dict(categoryorder='array', categoryarray=faixas_nomes))
fig_salario.update_traces(textposition="outside")
fig_salario.show()



sexo_freq = df["sexo"].value_counts(dropna=False).reset_index()
sexo_freq.columns = ["sexo", "quantidade"]
sexo_freq["percentual"] = (sexo_freq["quantidade"] / len(df) * 100).round(2)

fig_sexo = px.bar(
    sexo_freq,
    x="quantidade",
    y="sexo",
    orientation="h",
    text="percentual",
    title="Distribuição por Sexo",
    color="sexo",
    color_discrete_map={
        "Masculino": "#1f77b4",  # azul
        "Feminino": "#ff69b4",   # rosa
        "NA": "#808080",
        None: "#808080"
    }
)
fig_sexo.update_traces(texttemplate="%{text}%")
fig_sexo.update_layout(yaxis=dict(categoryorder='total ascending'))
fig_sexo.show()


df_cid = df.dropna(subset=["cidade"]).copy()
df_cid["cidade"] = df_cid["cidade"].str.title()

cid_freq = df_cid["cidade"].value_counts().reset_index()
cid_freq.columns = ["cidade", "quantidade"]

cid_top10 = cid_freq.head(10).sort_values(by="quantidade", ascending=True)


fig_cid_bar = px.bar(
    cid_top10,
    x="quantidade",
    y="cidade",
    orientation="h",
    text="quantidade",
    title="Top 10 Cidades — Quantidade de Pessoas",
    color="quantidade",
    color_continuous_scale="Teal"
)
fig_cid_bar.update_traces(textposition="outside")
fig_cid_bar.update_layout(yaxis=dict(categoryorder='total ascending'))
fig_cid_bar.show()

df_prof = df.dropna(subset=["profissao"]).copy()
df_prof["profissao"] = df_prof["profissao"].str.title()

prof_freq = df_prof["profissao"].value_counts().reset_index()
prof_freq.columns = ["profissao", "quantidade"]
prof_freq["percentual"] = (prof_freq["quantidade"] / len(df_prof) * 100).round(2)

salary_median = df_prof.groupby("profissao")["salario"].median().reset_index()
salary_median.columns = ["profissao", "salario_mediano"]

prof_final = pd.merge(prof_freq, salary_median, on="profissao")

prof_top10 = prof_final.head(10).sort_values(by="quantidade", ascending=True)

prof_top10["label_text"] = (
    prof_top10["quantidade"].astype(str) + 
    " | " + 
    prof_top10["percentual"].astype(str) + "% | R$ " +
    prof_top10["salario_mediano"].round(2).astype(str)
)

fig_prof = px.bar(
    prof_top10,
    x="quantidade",
    y="profissao",
    orientation="h",
    text="label_text",
    color="quantidade",
    color_continuous_scale="Blues",
    title="Top 10 Profissões — Quantidade, Percentual e Mediana Salarial"
)
fig_prof.update_layout(
    yaxis=dict(categoryorder='total ascending'),
    xaxis_title="Quantidade de Pessoas",
    yaxis_title="Profissão",
    coloraxis_colorbar_title="Qtd"
)
fig_prof.update_traces(textposition="outside")

fig_prof.show()

print("\n=== EDA Concluída com sucesso! ===")
