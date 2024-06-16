import osmnx as ox
import pandas as pd

# Definir o nome do lugar
place_name = "Porto, Portugal"

# Extrair dados de ruas
streets_graph = ox.graph_from_place(place_name, network_type='all')
edges = ox.graph_to_gdfs(streets_graph, nodes=False, edges=True, node_geometry=False, fill_edge_geometry=True)
df_streets = pd.DataFrame(edges)
df_streets.to_csv('porto_streets.csv', index=False)

# Extrair dados de lugares (POIs - Points of Interest)
# Por exemplo, lugares de interesse turístico, históricos, culturais, etc.
gdf_places = ox.geometries_from_place(place_name, tags={'tourism': True, 'historic': True, 'amenity': True})
df_places = pd.DataFrame(gdf_places)
df_places.to_csv('porto_places.csv', index=False)

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

# Converter para DataFrame
df_amenities = pd.DataFrame(gdf_amenities.drop(columns='geometry'))

# Salvar em CSV
df_amenities.to_csv('porto_amenities.csv', index=False)

print("Dados extraídos e salvos em arquivos CSV.")