import osmnx as ox
import geopandas as gpd
import pandas as pd

# Definir o nome do lugar
place_name = "Porto, Portugal"

# Extrair limites das freguesias
freguesias = ox.geocode_to_gdf(place_name, which_result=2)

# Verificar as colunas do GeoDataFrame das freguesias
print("Colunas das freguesias:", freguesias.columns)

# Certifique-se de que a coluna 'name' ou uma coluna apropriada exista
if 'name' not in freguesias.columns:
    # Se 'name' não estiver disponível, verifique outras colunas possíveis
    print("Colunas disponíveis nas freguesias:", freguesias.columns)
    # Alterar 'name' para a coluna apropriada, se necessário
    freguesia_name_col = freguesias.columns[0]
else:
    freguesia_name_col = 'display_name'

# Extrair dados de amenidades
amenity_tags = {
    'amenity': [
        'school', 'hospital', 'university', 'college', 'clinic', 'nursing_home', 'kindergarten', 
        'community_centre', 'library', 'place_of_worship', 'police', 'fire_station', 'post_office',
        'townhall', 'marketplace', 'bank', 'atm', 'pharmacy', 'dentist', 'doctors', 'cafe', 'restaurant'
    ]
}

gdf_amenities = ox.geometries_from_place(place_name, tags=amenity_tags)

# Extrair dados de edifícios
gdf_buildings = ox.geometries_from_place(place_name, tags={'building': True})

# Certificar-se de que os DataFrames estejam no mesmo sistema de referência de coordenadas (CRS)
gdf_amenities = gdf_amenities.to_crs(freguesias.crs)
gdf_buildings = gdf_buildings.to_crs(freguesias.crs)

# Fazer uma interseção espacial para atribuir amenidades e edifícios às freguesias
gdf_amenities_freguesias = gpd.sjoin(gdf_amenities, freguesias, how='inner', predicate='within')
gdf_buildings_freguesias = gpd.sjoin(gdf_buildings, freguesias, how='inner', predicate='within')

# Função para extrair informações detalhadas
def extract_details(gdf, type_col):
    data = {
        'Type': [],
        'Location': [],
        'Neighborhood': [],
        'Residential': [],
        'Shop': [],
        'Work': [],
        'Latitude': [],
        'Longitude': []
    }
    for idx, row in gdf.iterrows():
        data['Type'].append(row.get(type_col, ''))
        data['Location'].append(row.get('addr:street', ''))
        data['Neighborhood'].append(row[freguesia_name_col])
        data['Residential'].append(row.get('building', '') if type_col == 'building' else '')
        data['Shop'].append(row.get('shop', ''))
        data['Work'].append(row.get('office', ''))
        data['Latitude'].append(row.geometry.centroid.y)
        data['Longitude'].append(row.geometry.centroid.x)
    return pd.DataFrame(data)

# Extrair detalhes das amenidades e edifícios
df_amenities_details = extract_details(gdf_amenities_freguesias, 'amenity')
df_buildings_details = extract_details(gdf_buildings_freguesias, 'building')

# Salvar os dados em arquivos CSV
df_amenities_details.to_csv('porto_amenities_details.csv', index=False)
df_buildings_details.to_csv('porto_buildings_details.csv', index=False)

print("Dados de amenidades e edifícios extraídos e salvos em CSV com detalhes.")
