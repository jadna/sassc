import pandas as pd

# Exemplo de criação de dataframes
df1 = pd.read_csv('./data/porto_amenities_with_freguesia.csv')
df2 = pd.read_csv('./data/porto_buildings_with_freguesia.csv')
df3 = pd.read_csv('./data/porto_pois_with_freguesia.csv')
df4 = pd.read_csv('./data/porto_places.csv')
df5 = pd.read_csv('./data/porto_amenities.csv')
df6 = pd.read_csv('./data/porto_shops.csv')

# Concatenar os dataframes
df_concat = pd.concat([df1, df2, df3, df4, df5, df6])

# Remover as linhas duplicadas
df_unique = df_concat.drop_duplicates(subset=['name','type','freguesia'])

# Ordenando o DataFrame pela coluna 'A'
df_sorted = df_unique.sort_values(by='type')

print(df_sorted)
df_sorted.to_csv('./data/resultado.csv', index=False)