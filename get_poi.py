import osmnx as ox
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Configurar logging para depuração
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Definir a localização - Porto, Portugal
city = "Porto, Portugal"

# Configurar os parâmetros de consulta para POIs
pois_tags = {'amenity': True, 'shop': True, 'tourism': True, 'leisure': True}

# Baixar os dados dos POIs
logger.info("Baixando dados dos POIs...")
try:
    pois = ox.geometries_from_place(city, pois_tags)
    logger.info(f"Número de POIs encontrados: {len(pois)}")
except Exception as e:
    logger.error(f"Erro ao baixar dados dos POIs: {e}")
    pois = None

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

if pois is not None and admin_boundaries is not None:
    # Preparar os dados dos POIs
    data = []
    for idx, row in pois.iterrows():
        name = row.get('name', None)
        poi_type = row.get('amenity') or row.get('shop') or row.get('tourism') or row.get('leisure')
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

        data.append([name, poi_type, address, latitude, longitude, freguesia, opening_hours])

    # Criar um DataFrame e salvar em um arquivo CSV
    df = pd.DataFrame(data, columns=['name', 'type', 'address', 'latitude', 'longitude', 'freguesia', 'opening_hours'])
    df.to_csv('./data/porto_pois_with_freguesia.csv', index=False)
    logger.info("Arquivo CSV salvo com sucesso.")
else:
    logger.error("Não foi possível obter os dados necessários.")
