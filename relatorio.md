#  Projeto de Big Data – Análise Exploratória e Dashboard Interativo

##  Autor
Leonardo Santana  
Curso: Análise e Desenvolvimento de Sistemas  
Instituição: Estácio  

---

# 1. Introdução

Este projeto tem como objetivo realizar o tratamento, análise exploratória (EDA) e visualização interativa de um conjunto de dados contendo informações demográficas, profissionais e salariais de indivíduos.

Além das análises, foi desenvolvido um **dashboard interativo em Streamlit**, permitindo explorar os dados de maneira dinâmica e amigável.

O trabalho está dividido em:

1. Limpeza e padronização dos dados  
2. Análise exploratória (EDA)  
3. Construção do dashboard  
4. Preparação para clusterização (Etapa 3)  

---

# 🛠 2. Estrutura do Projeto

Projeto_Big_Data/
├── data/
│ └── lista2.xls
├── src/
│ ├── data_processing.py
│ ├── eda.py
│ └── app.py
└── relatorio.md


---

# 3. Tratamento e Limpeza dos Dados

O ETL foi realizado no arquivo `data_processing.py`, seguindo as etapas:

### ✔ Padronização dos nomes das colunas  
Todas as colunas foram convertidas para minúsculas.

### ✔ Conversão da data de nascimento  
Formato reconhecido e convertido para `datetime`.

### ✔ Cálculo da idade  
Criada coluna “idade” baseada em `dt_nasc`.

### ✔ Remoção de registros inválidos  
Linhas sem idade, sem salário ou com valores inconsistentes foram removidas.

### ✔ Eliminação de coluna inútil  
A coluna `unnamed:_14` foi excluída.

### ✔ Total final de registros  
**Registros originais:** 7.641  
**Registros após limpeza:** 7.545  

---

# 4. Análise Exploratória (EDA)

A EDA foi desenvolvida no arquivo `eda.py`.  
Os principais achados estão descritos abaixo.

---

# 4.1 Distribuição de Idade

O histograma demonstra que a maioria dos indivíduos possui idade entre 50 e 70 anos.

Pontos importantes:
- Predomínio da faixa etária adulta e idosa.  
- Baixa quantidade de jovens no conjunto de dados.  

---

# 4.2 Faixa Salarial

Criamos faixas de salário:

- **0–2k**  
- **2–4k**  
- **4–6k**  
- **6–10k**  
- **10k+**

Principais observações:

- A maior parte dos salários se concentra entre **2k e 6k**.
- Poucos indivíduos acima de 10k.
- Distribuição típica de servidores operacionais e administrativos.

---

# 4.3 Distribuição por Sexo (Gráfico Especial)

Implementamos um gráfico personalizado:

- Barras horizontais  
- Ícones 👨 e 👩  
- Azul para masculino  
- Rosa para feminino  
- Percentuais destacados  

Resultado:

- Predominância do sexo **feminino**.
- Proporção aproximadamente:
  - 72–73% Feminino  
  - 27–28% Masculino  

---

# 4.4 Top 10 Cidades

As cidades com maior registro foram:

1. **Rio de Janeiro** (RJ)  
2. Nilópolis  
3. Nova Iguaçu  
4. São Gonçalo  
5. Duque de Caxias  
6. Niterói  
7. Nova Friburgo  
8. Macaé  
9. Campos  
10. Angra dos Reis  

Essas cidades representam a maior densidade populacional e administrativa do estado.

---

# 4.5 Profissões Mais Frequentes

O Top 10 inclui cargos como:

- Merendeira  
- Agente de Portaria  
- Art. de Cozinha  
- Auxiliar Administrativo  
- Professor  
- Auxiliar de Serviços Gerais  

A distribuição reforça a predominância de atividades públicas operacionais.

---

# Dashboard Interativo (Streamlit)

O arquivo `app.py` integra todas as visualizações, incluindo:

- Filtros de UF  
- Gráfico de idade  
- Faixa salarial  
- Gráfico especial de sexo  
- Top cidades  
- Top profissões  

Com isso, o usuário pode navegar interativamente entre diferentes visões do conjunto de dados.

Para executar:


---

# 6. Conclusões

- Os dados exigiam limpeza significativa, especialmente datas e salários.  
- A população analisada possui forte predominância feminina.  
- A faixa salarial principal está entre 2 mil e 6 mil reais.  
- Profissões e cidades refletem o perfil administrativo do estado.  
- O dashboard facilita a exploração visual e rápida das informações.

---

# 7. Próxima Etapa: Clusterização (ETAPA 3)

A etapa seguinte do projeto envolve:

- Selecionar variáveis  
- Padronizar os dados (scaling)  
- Aplicar K-Means  
- Visualizar os clusters  
- Interpretar grupos socioeconômicos  

Assim que você disser **“Quero a etapa 3”**, entraremos na fase de clusterização.

---

# 8. Tecnologias Utilizadas

- Python  
- Pandas  
- Plotly  
- Streamlit  
- NumPy  
- Scikit-Learn (próxima etapa)

---

#  Projeto desenvolvido por:
**Leonardo Santana**  
Estudante de Análise e Desenvolvimento de Sistemas  
