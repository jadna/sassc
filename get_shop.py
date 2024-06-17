import osmnx as ox
import pandas as pd

# Definir o nome do lugar
place_name = "Porto, Portugal"

# Extrair dados de amenities com a tag 'shop'
tags = {
    'shop': True  # Todas as lojas
}

# Extrair dados do OSM
gdf = ox.features_from_place(place_name, tags=tags)

# Adicionar colunas de latitude e longitude
gdf['latitude'] = gdf.geometry.centroid.y
gdf['longitude'] = gdf.geometry.centroid.x

# Preencher informações adicionais
gdf['name'] = gdf['name'].fillna('')

# O tipo de loja já está na tag 'shop'
gdf['type'] = gdf['shop']

# Preencher endereço
gdf['addr:street'] = gdf['addr:street'].fillna('')
gdf['addr:housenumber'] = gdf['addr:housenumber'].fillna('')
gdf['address'] = gdf['addr:street'] + ' ' + gdf['addr:housenumber']

# Preencher cidade
gdf['city'] = gdf.get('addr:city', None)

# Preencher bairro
gdf['freguesia'] = gdf.get('addr:suburb', None)


# Preencher horário de funcionamento
gdf['opening_hours'] = gdf.get('opening_hours', None)

# Selecionar colunas desejadas
columns = ['name', 'type', 'address', 'latitude', 'longitude', 'freguesia', 'opening_hours']
df = gdf[columns]

# Salvar em CSV
df.to_csv('./data/porto_shops.csv', index=False)

print("Dados extraídos e salvos em porto_shops.csv")
