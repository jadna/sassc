import osmnx as ox
import pandas as pd

# Definir o nome do lugar
place_name = "Porto, Portugal"

# Extrair dados de amenidades e POIs
tags = {
    'amenity': True,    # Todas as amenities
    'tourism': True,    # Pontos turísticos
    'historic': True,   # Locais históricos
    'shop': True        # Lojas
}

# Extrair dados do OSM
gdf = ox.geometries_from_place(place_name, tags=tags)

# Adicionar colunas de latitude e longitude
gdf['latitude'] = gdf.geometry.centroid.y
gdf['longitude'] = gdf.geometry.centroid.x

# Preencher informações adicionais
gdf['name'] = gdf['name'].fillna('')

# Combinar os tipos de amenities e POIs
gdf['type'] = gdf['amenity'].combine_first(gdf['tourism']).combine_first(gdf['historic']).combine_first(gdf['shop'])

# Endereço
gdf['addr:street'] = gdf['addr:street'].fillna('')
gdf['addr:housenumber'] = gdf['addr:housenumber'].fillna('')
gdf['address'] = gdf['addr:street'] + ' ' + gdf['addr:housenumber']

# Cidade
gdf['addr:city'] = gdf['addr:city'].fillna('Porto')
gdf['city'] = gdf['addr:city']

# Bairro
gdf['neighborhood'] = gdf['addr:suburb'].fillna('')
# gdf['addr:quarter'] = gdf['addr:quarter'].fillna('')
# gdf['neighborhood'] = gdf['addr:suburb'].combine_first(gdf['addr:quarter'])

# Horário de Funcionamento
gdf['opening_hours'] = gdf['opening_hours'].fillna('')

# Selecionar colunas desejadas
columns = ['name', 'type', 'address', 'latitude', 'longitude', 'city', 'neighborhood', 'opening_hours']
df = gdf[columns]

# Salvar em CSV
df.to_csv('porto_amenities_pois.csv', index=False)

print("Dados extraídos e salvos em porto_amenities_pois.csv")
