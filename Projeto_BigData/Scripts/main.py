import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Pega o caminho absoluto da pasta onde o script está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Monta o caminho para a planilha independente da máquina
excel_path = os.path.join(BASE_DIR, "../Dados/lista2.xlsx")

df = pd.read_excel(excel_path)

df_numerico = df.select_dtypes(include=['float64', 'int64'])

print(df_numerico.head())

plt.figure(figsize=(10,8))
sns.heatmap(df_numerico.corr(), annot=True, cmap='coolwarm', square=True)
plt.title('Matriz de Correlação (Somente Variáveis Numéricas)')
plt.show()
