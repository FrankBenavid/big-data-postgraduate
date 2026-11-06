"""Prepara ejemplos a partir de archivos DANE MGN 2025 y EVA UPRA descargados.
Uso: python preparar_capas.py municipios.zip eva.csv carpeta_salida
"""
from pathlib import Path
import sys
import geopandas as gpd
import pandas as pd

zip_path, eva_path, output = sys.argv[1:]
out = Path(output)
out.mkdir(parents=True, exist_ok=True)
x = gpd.read_file(f"zip://{Path(zip_path).resolve()}")
x = x.loc[x.dpto_ccdgo == '15'].copy().to_crs(9377)
x['area_km2'] = x.geometry.area / 1e6
x['geometry'] = x.geometry.simplify(75, preserve_topology=True)
x = x[['mpio_cdpmp', 'mpio_cnmbr', 'area_km2', 'geometry']].rename(
    columns={'mpio_cdpmp': 'codigo_municipio', 'mpio_cnmbr': 'municipio_mgn'})
x.to_crs(4326).to_file(out / 'municipios_boyaca_mgn_2025.geojson', driver='GeoJSON')
y = pd.read_csv(eva_path)
y = y.loc[(y['Código Dane departamento'] == 15) & (y['Año'] == 2024) &
          (y['Desagregación cultivo'] == 'Papa todas las variedades')].copy()
y = y.rename(columns={'Código Dane municipio': 'codigo_municipio', 'Municipio': 'municipio',
    'Año': 'anio', 'Periodo': 'periodo', 'Área cosechada': 'area_cosechada_ha',
    'Producción': 'produccion_t', 'Estado físico del cultivo': 'estado_fisico',
    'Desagregación cultivo': 'producto'})
y['codigo_municipio'] = y['codigo_municipio'].astype(str).str.zfill(5)
y[['codigo_municipio', 'municipio', 'anio', 'periodo', 'producto', 'estado_fisico',
   'area_cosechada_ha', 'produccion_t']].to_csv(out / 'eva_papa_boyaca_2024.csv', index=False)
