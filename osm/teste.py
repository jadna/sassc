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
gdf_amenities = ox.geometries_from_place(place_name, tags={
    'amenity': ['school', 'hospital', 'university', 'college', 'clinic', 'nursing_home', 'kindergarten', 
        'community_centre', 'library', 'place_of_worship', 'police', 'fire_station', 'post_office',
        'townhall', 'marketplace', 'bank', 'atm', 'pharmacy', 'dentist', 'doctors', 'building']
})
df_amenities = pd.DataFrame(gdf_amenities)
df_amenities.to_csv('porto_amenities1.csv', index=False)

print("Dados extraídos e salvos em arquivos CSV.")
