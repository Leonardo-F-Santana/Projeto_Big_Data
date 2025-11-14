import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_excel('./lista2.xls')
print(df.head())


plt.figure(figsize=(10,8))
sns.scatterplot(df.corr(), annot=True, cmap='coolwarm', square=True)
plt.title('Gráfico de calor')
plt.show()
