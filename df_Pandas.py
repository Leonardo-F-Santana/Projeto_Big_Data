import pandas as pd
'''json_array = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]

df = pd.DataFrame(json_array)
print(df)'''


df = pd.DataFrame({'Animal': ['Cachorro', 'Gato','Cachorro', 'Gato'], 'Velocidade': [45., 30., 40., 35.]})
agrupado = df.groupby(['Animal'])
print(agrupado.mean())
print(agrupado.agg({'Velocidade': 'mean'}))
print(agrupado.agg({'Velocidade': ['min', 'max']}))