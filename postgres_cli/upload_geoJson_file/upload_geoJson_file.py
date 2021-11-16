# Just run this cript to upload one geojson file to the postgis database # Imports
from geoalchemy2 import Geometry, WKTElement
from shapely.geometry import geo
from sqlalchemy import *
import pandas as pd
import geopandas as gpd
import extract_info
import count_number_of_rows
import pprint
from geopandas import GeoSeries
from shapely.geometry import Polygon
import itertools
import os
import find_ortho_of_the_label
import get_ortho_file_id_with_query


if __name__ == '__main__':
    # Creating SQLAlchemy's engine to use
    engine = create_engine('postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres_backup')

    _URL_ = r'c:\Users\hasan\OneDrive\Masaüstü\Label__Dist_12_13__winter__v2.geojson'
    ortho_url = find_ortho_of_the_label.find_ortho(_URL_)[0]
    ortho_id = get_ortho_file_id_with_query.get_raster_id(ortho_url)

    url = repr(os.path.abspath(_URL_))[1:-1]
    url_tuple = (url, 993280764)
    label_session_table_number_of_rows = count_number_of_rows.count_rows_of_table('label_session')
    id_label_session_iter = itertools.count(label_session_table_number_of_rows)
    next(id_label_session_iter)

    label_table_number_of_rows = count_number_of_rows.count_rows_of_table('label')
    id_label_iter = itertools.count(label_table_number_of_rows)
    next(id_label_iter)

    label_feature_table_number_of_rows = count_number_of_rows.count_rows_of_table('label_feature')
    id_label_feature_iter = itertools.count(label_feature_table_number_of_rows)
    next(id_label_feature_iter)

    label_session_table_gdf, label_table_gdf, label_feature_table_gdf = extract_info.get_data_geoJson(url_tuple, id_label_session_iter, id_label_iter, id_label_feature_iter)

    # upload label_session_table
    label_session_table_gdf['session_area'] = label_session_table_gdf['geom'].apply(lambda x: WKTElement(x.wkt, srid=4326))
    label_session_table_gdf.drop('geom', 1, inplace=True)
    label_session_table_gdf.to_sql('label_session', engine, if_exists='append', index=False, dtype={'session_area': Geometry('POINT', srid= 4326)})

    # upload label_table 
    label_table_gdf['label_area_epsg_4326'] = label_table_gdf['geom_EPSG4326'].apply(lambda x: WKTElement(x.wkt, srid=4326))
    label_table_gdf['label_area_epsg_3857'] = label_table_gdf['geom_EPSG3857'].apply(lambda x: WKTElement(x.wkt, srid=3857))
    label_table_gdf.drop('geom_EPSG4326', 1, inplace=True)
    label_table_gdf.drop('geom_EPSG3857', 1, inplace=True)
    label_table_gdf.to_sql('label', engine, if_exists='append', index=False, dtype={'label_area_epsg_4326': Geometry('POINT', srid= 4326), 'label_area_epsg_3857': Geometry('POINT', srid= 3857)})

    # upload label_feature_table
    label_feature_table_gdf['feature_area'] = label_feature_table_gdf['geom'].apply(lambda x: WKTElement(x.wkt, srid=4326))
    label_feature_table_gdf.drop('geom', 1, inplace=True)
    label_feature_table_gdf.to_sql('label_feature', engine, if_exists='append', index=False, dtype={'feature_area': Geometry('POINT', srid= 4326)})


