import pandas as pd

# Exemplo de criação de dataframes
df1 = pd.read_csv('./data/porto_amenities_with_freguesia.csv')
df2 = pd.read_csv('./data/porto_buildings_with_freguesia.csv')
df3 = pd.read_csv('./data/porto_pois_with_freguesia.csv')
df4 = pd.read_csv('./data/porto_places.csv')
df5 = pd.read_csv('./data/porto_amenities.csv')

# Concatenar os dataframes
df_concat = pd.concat([df1, df2, df3, df4, df5])

# Remover as linhas duplicadas
df_unique = df_concat.drop_duplicates()

print(df_unique)
df_unique.to_csv('./data/resultado.csv', index=False)