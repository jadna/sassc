import osmnx as ox
import pandas as pd

# Definir o nome do lugar
place_name = "Porto, Portugal"

# Extrair dados de ruas
streets_graph = ox.graph_from_place(place_name, network_type='all')
edges = ox.graph_to_gdfs(streets_graph, nodes=False, edges=True, node_geometry=False, fill_edge_geometry=True)
# Adicionar colunas de latitude e longitude
edges['latitude'] = edges.geometry.centroid.y
edges['longitude'] = edges.geometry.centroid.x

# Extrair informações específicas: nome, type, endereço, latitude, longitude, freguesia e horário de abertura
# Verificar se as colunas existem e renomear se necessário
edges['name'] = edges.get('name', None)
edges['highway'] = edges.get('highway', None)
edges['maxspeed'] = edges.get('maxspeed', None)
edges['length'] = edges.get('length', None)
edges['bridge'] = edges.get('bridge', None)
edges['service'] = edges.get('service', None)
edges['tunnel'] = edges.get('tunnel', None)

# Selecionar colunas necessárias
columns = ['name', 'highway', 'maxspeed', 'latitude', 'longitude', 'length', 'bridge', 'service', 'tunnel']
edges = edges[columns]

df_streets = pd.DataFrame(edges)
df_streets.to_csv('./data/porto_streets.csv', index=False)

# Extrair dados de lugares (POIs - Points of Interest)
# Por exemplo, lugares de interesse turístico, históricos, culturais, etc.
gdf_places = ox.geometries_from_place(place_name, tags={'tourism': True, 'historic': True, 'amenity': True})

# Adicionar colunas de latitude e longitude
gdf_places['latitude'] = gdf_places.geometry.centroid.y
gdf_places['longitude'] = gdf_places.geometry.centroid.x

# Extrair informações específicas: nome, type, endereço, latitude, longitude, freguesia e horário de abertura
# Verificar se as colunas existem e renomear se necessário
gdf_places['name'] = gdf_places.get('name', None)
gdf_places['type'] = gdf_places.get('amenity', None)
gdf_places['address'] = gdf_places.get('addr:street', None)
gdf_places['freguesia'] = gdf_places.get('addr:suburb', None)
gdf_places['opening_hours'] = gdf_places.get('opening_hours', None)

# Selecionar colunas necessárias
columns = ['name', 'type', 'address', 'latitude', 'longitude', 'freguesia', 'opening_hours']
gdf_places = gdf_places[columns]
df_places = pd.DataFrame(gdf_places)
df_places.to_csv('./data/porto_places.csv', index=False)

# Extrair dados de amenidades que podem representar informações demográficas
# Exemplo: escolas, hospitais, universidades
amenity_tags = {
    'amenity': [
        "school", "university", "kindergarten", "college", "library",        # Educação
        "hospital", "clinic", "doctors", "dentist", "pharmacy", "veterinary", # Saúde
        "fire_station", "police", "post_office", "townhall",                 # Serviços Públicos
        "arts_centre", "cinema", "theatre", "community_centre", "museum", "nightclub", "park", # Lazer e Cultura
        "bank", "atm", "cafe", "restaurant", "fast_food", "bar", "pub", "marketplace", "fuel", "car_wash", "car_rental", # Comércio e Serviços
        "bus_station", "taxi", "ferry_terminal", "bicycle_rental", "charging_station",  # Transportes
        "hotel", "guest_house", "hostel", "motel", "camp_site",  "caravan_site", # Serviços de Hospedagem
        "place_of_worship", "church", "mosque", "synagogue", "temple",       # Serviços Religiosos
        "social_facility", "nursing_home", "childcare", "food_bank", "shelter", # Serviços Sociais
        "toilets", "shower", "drinking_water", "telephone", "waste_basket", "recycling", "bench", "parking", "bicycle_parking"  # Outros
    ]
}

gdf_amenities = ox.geometries_from_place(place_name, tags=amenity_tags)

# Adicionar colunas de latitude e longitude
gdf_amenities['latitude'] = gdf_amenities.geometry.centroid.y
gdf_amenities['longitude'] = gdf_amenities.geometry.centroid.x

# Extrair informações específicas: nome, type, endereço, latitude, longitude, freguesia e horário de abertura
# Verificar se as colunas existem e renomear se necessário
gdf_amenities['name'] = gdf_amenities.get('name', None)
gdf_amenities['type'] = gdf_amenities.get('amenity', None)
gdf_amenities['address'] = gdf_amenities.get('addr:street', None)
gdf_amenities['freguesia'] = gdf_amenities.get('addr:suburb', None)
gdf_amenities['opening_hours'] = gdf_amenities.get('opening_hours', None)

# Selecionar colunas necessárias
columns = ['name', 'type', 'address', 'latitude', 'longitude', 'freguesia', 'opening_hours']
df_amenities = gdf_amenities[columns]

# Salvar em CSV
df_amenities.to_csv('./data/porto_amenities.csv', index=False)

print("Dados extraídos e salvos em arquivos CSV.")
