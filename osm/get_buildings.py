import osmnx as ox
import pandas as pd

# Definir o nome do lugar
place_name = "Porto, Portugal"

# Extrair dados de edifícios com tags específicas
tags = {'building': True}

# Extrair geometrias dos edifícios
gdf_buildings = ox.geometries_from_place(place_name, tags=tags)

# Criar um DataFrame com as colunas desejadas: nome, endereço, freguesia, latitude e longitude
df_buildings = pd.DataFrame({
    'name': gdf_buildings['name'],  # Nome do edifício, se disponível
    'address': gdf_buildings['addr:street'],  # Endereço completo, se disponível
    # 'freguesia': gdf_buildings['addr:subdistrict'],  # Freguesia (bairro), se disponível
    'latitude': gdf_buildings.geometry.centroid.y,  # Latitude do ponto central do edifício
    'longitude': gdf_buildings.geometry.centroid.x  # Longitude do ponto central do edifício
})

# Exibir primeiras linhas do DataFrame
print(df_buildings.head())

# Salvar DataFrame em um arquivo CSV
df_buildings.to_csv('porto_buildings.csv', index=False)
