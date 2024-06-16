import osmnx as ox
import pandas as pd

# Definir o nome do lugar
place_name = "Porto, Portugal"

# Extrair dados de amenidades
amenity_tags = {
    'amenity': [
        'school', 'hospital', 'university', 'college', 'clinic', 'nursing_home', 'kindergarten', 
        'community_centre', 'library', 'place_of_worship', 'police', 'fire_station', 'post_office',
        'townhall', 'marketplace', 'bank', 'atm', 'pharmacy', 'dentist', 'doctors'
    ]
}

gdf_amenities = ox.geometries_from_place(place_name, tags=amenity_tags)

# Converter GeoDataFrame para DataFrame
df_amenities = pd.DataFrame(gdf_amenities)

# Exibir primeiras linhas do DataFrame
print(df_amenities.head())

# Salvar DataFrame em um arquivo CSV
df_amenities.to_csv('porto_amenities.csv', index=False)

print("Dados de amenidades extraídos e salvos em porto_amenities.csv.")
