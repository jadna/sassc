import logging
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import osmnx as ox

# Configurar logging para depuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Definir a localização - Porto, Portugal
city = "Porto, Portugal"

# Configurar os parâmetros de consulta para prédios
building_tags = {'building': True}

# Baixar os dados dos prédios
logger.info("Baixando dados dos prédios...")
try:
    buildings = ox.geometries_from_place(city, building_tags)
    logger.info(f"Número de prédios encontrados: {len(buildings)}")
except Exception as e:
    logger.error(f"Erro ao baixar dados dos prédios: {e}")
    buildings = None

# Baixar os dados das freguesias
administrative_tags = {'boundary': 'administrative', 'admin_level': '9'}  # admin_level=9 é geralmente usado para freguesias em Portugal

logger.info("Baixando dados das freguesias...")
try:
    admin_boundaries = ox.geometries_from_place(city, administrative_tags)
    admin_boundaries = admin_boundaries.to_crs(epsg=4326)
    logger.info(f"Número de freguesias encontradas: {len(admin_boundaries)}")
except Exception as e:
    logger.error(f"Erro ao baixar dados das freguesias: {e}")
    admin_boundaries = None

if buildings is not None and admin_boundaries is not None:
    # Preparar os dados dos prédios
    data = []
    for idx, row in buildings.iterrows():
        name = row.get('name', None)
        building_type = row.get('building', None)
        address = row.get('addr:full', None)
        if not address:
            street = row.get('addr:street', None)
            housenumber = row.get('addr:housenumber', None)
            address = f"{housenumber} {street}".strip()
        latitude = row.geometry.centroid.y if row.geometry else None
        longitude = row.geometry.centroid.x if row.geometry else None
        opening_hours = row.get('opening_hours', None)
        freguesia = None

        # Determinar a freguesia
        if row.geometry:
            point = gpd.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[row.geometry.centroid])
            for _, admin_row in admin_boundaries.iterrows():
                if admin_row.geometry.contains(point.iloc[0].geometry):
                    freguesia = admin_row.get('name', None)
                    break

        data.append([name, building_type, address, latitude, longitude, opening_hours, freguesia])

    # Criar um DataFrame e salvar em um arquivo CSV
    df = pd.DataFrame(data, columns=['name', 'type', 'address', 'latitude', 'longitude', 'opening_hours', 'freguesia'])
    df.to_csv('./data/porto_buildings_with_freguesia.csv', index=False)
    logger.info("Arquivo CSV salvo com sucesso.")
else:
    logger.error("Não foi possível obter os dados necessários.")
