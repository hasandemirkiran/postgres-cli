# Imports
from geoalchemy2 import Geometry, WKTElement
from shapely.geometry import geo
from sqlalchemy import *
import pandas as pd
import geopandas as gpd
import extract_info_windows
import pprint
from geopandas import GeoSeries
from shapely.geometry import Polygon

# Creating SQLAlchemy's engine to use
engine = create_engine(
    "postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres_hasan"
)
path = "\\\\192.168.37.4\\gis_data"


label_df_list = extract_info_windows.pick_all_geojson()
for label_session_table_gdf, label_table_gdf, label_feature_table_gdf in label_df_list:
    # upload label_session_table
    label_session_table_gdf["session_area"] = label_session_table_gdf["geom"].apply(
        lambda x: WKTElement(x.wkt, srid=4326)
    )
    label_session_table_gdf.drop("geom", 1, inplace=True)
    label_session_table_gdf.to_sql(
        "label_session",
        engine,
        if_exists="append",
        index=False,
        dtype={"session_area": Geometry("POINT", srid=4326)},
    )

    # upload label_table
    label_table_gdf["label_area_EPSG4326"] = label_table_gdf["geom_EPSG4326"].apply(
        lambda x: WKTElement(x.wkt, srid=4326)
    )
    label_table_gdf["label_area_EPSG3857"] = label_table_gdf["geom_EPSG3857"].apply(
        lambda x: WKTElement(x.wkt, srid=4326)
    )
    label_table_gdf.drop("geom_EPSG4326", 1, inplace=True)
    label_table_gdf.drop("geom_EPSG3857", 1, inplace=True)
    label_table_gdf.to_sql(
        "label",
        engine,
        if_exists="append",
        index=False,
        dtype={
            "label_area_EPSG4326": Geometry("POINT", srid=4326),
            "label_area_EPSG3857": Geometry("POINT", srid=3857),
        },
    )

    # upload label_feature_table
    label_feature_table_gdf["feature_area"] = label_feature_table_gdf["geom"].apply(
        lambda x: WKTElement(x.wkt, srid=4326)
    )
    label_feature_table_gdf.drop("geom", 1, inplace=True)
    label_feature_table_gdf.to_sql(
        "label_feature",
        engine,
        if_exists="append",
        index=False,
        dtype={"feature_area": Geometry("POINT", srid=4326)},
    )
    # label_feature_table_gdf.to_sql('label_feature', con = engine, if_exists='append', index=False)

"""
# print(label_session_table_gdf)
# print()
# print(label_table_gdf)
# print()
# print(label_feature_table_gdf['geom'][0])

"""
