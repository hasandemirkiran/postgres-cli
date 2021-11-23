import geopandas as gpd
import pprint
from pyproj import Transformer
import geojson
from shapely.geometry import box
from sqlalchemy import *
from sqlalchemy.sql.expression import label
import itertools
from postgres_cli.upload_geoJson_file import count_number_of_rows
import pprint
import os

def get_data_geoJson(
    url_tuple, id_label_session_iter, id_label_iter, id_label_feature_iter
):

    url = url_tuple[0]

    class_dict = {
        "Douglas": 0,
        "Fir": 1,
        "Larch": 2,
        "Spruce": 3,
        "Pine": 4,
        "Leaved Tree": 5,
        "Dead Tree": 6,
        "Young Tree": 7,
        "Background": 8,
        "Unknown": 9,
        "done": 10,
        "Dead Pine": 11,
        "Douglas fir": 12,
        "healthy": 13,
        "dead": 14,
        "affected": 15,
        "no class": 16,
    }

    geojson_gpd = gpd.read_file(url)

    # --- label_session table entries ---
    label_session_table_id = []
    label_session_table_id.append(next(id_label_session_iter))
    label_session_table_session_area = []
    b = box(
        geojson_gpd.total_bounds.tolist()[0],
        geojson_gpd.total_bounds.tolist()[2],
        geojson_gpd.total_bounds.tolist()[1],
        geojson_gpd.total_bounds.tolist()[3],
    )
    label_session_table_session_area.append(b)
    label_session_table_raster_info_id = []
    label_session_table_raster_info_id.append(url_tuple[1])
    label_session_table_name = []
    name = url.split(r"/")[-1].split("__")[1]
    label_session_table_name.append(name)

    label_session_table_df = gpd.GeoDataFrame(
        list(
            zip(
                label_session_table_id,
                label_session_table_name,
                label_session_table_session_area,
                label_session_table_raster_info_id,
            )
        ),
        columns=["id", "name", "geom", "raster_info_id"],
    )

    # --- label table entries ---
    num_of_bbox = geojson_gpd.bbox_id.values.max() + 1
    label_table_id = [next(id_label_iter) for x in range(num_of_bbox)]
    label_table_session_id = [label_session_table_id[0] for x in range(num_of_bbox)]

    with open(url) as f:
        geojson_gpd_2 = geojson.load(f)
    label_table_label_area_EPSG3857 = geojson_gpd_2["boxes"]
    label_table_label_area_EPSG4326 = []
    transformer = Transformer.from_crs(3857, 4326)
    for x in label_table_label_area_EPSG3857:
        points_tuple = ((x[0], x[1]), (x[2], x[3]))
        point_to_add = []
        for pt in transformer.itransform(points_tuple):
            point_to_add.append(pt[0])
            point_to_add.append(pt[1])
        label_table_label_area_EPSG4326.append(point_to_add)

    label_table_label_area_EPSG3857 = [
        box(x[0], x[2], x[1], x[3]) for x in label_table_label_area_EPSG3857
    ]
    label_table_label_area_EPSG4326 = [
        box(x[0], x[2], x[1], x[3]) for x in label_table_label_area_EPSG4326
    ]
    label_table_df = gpd.GeoDataFrame(
        list(
            zip(
                label_table_id,
                label_table_session_id,
                label_table_label_area_EPSG4326,
                label_table_label_area_EPSG3857,
            )
        ),
        columns=["id", "session_id", "geom_EPSG4326", "geom_EPSG3857"],
    )

    # dict to use in label_feature table while finding the label_feature_table_label_id
    list_id = []
    list_geom = []
    for index, row in label_table_df.iterrows():
        list_id.append(row["id"])
        list_geom.append(row["geom_EPSG3857"])
    # fetch a row with a value from label_table_df
    # print(label_table_df.loc[label_table_df.label_area_EPSG3857.apply(lambda x: x == [1396989.2801922676, 6191713.417884247, 1397035.0114690675,6191759.284482648])])

    # ---label_feature table ---
    label_feature_class = geojson_gpd.loc[:, "class"]

    label_feature_table_id = [
        next(id_label_feature_iter) for x in range(len(label_feature_class))
    ]

    label_features_bbox_id = geojson_gpd.loc[:, "bbox_id"]
    label_features_bbox_EPSG3857 = [
        label_table_label_area_EPSG3857[x] for x in label_features_bbox_id
    ]
    label_feature_table_label_id = [
        list_id[list_geom.index(geom)] for geom in label_features_bbox_EPSG3857
    ]

    label_feature_table_feature_area = geojson_gpd.loc[:, "geometry"]
    label_feature_table_class_id = [class_dict[x] for x in label_feature_class]
    label_feature_table_df = gpd.GeoDataFrame(
        list(
            zip(
                label_feature_table_id,
                label_feature_table_label_id,
                label_feature_table_feature_area,
                label_feature_table_class_id,
            )
        ),
        columns=["id", "label_id", "geom", "class_id"],
    )

    return (label_session_table_df, label_table_df, label_feature_table_df)

    # gpd.GeoDataFrame({'id': id, 'class_id': class_series_ids,'geom':  feature_area_series,'label_id': bbox_id_series})


if __name__ == "__main__":
    url = repr(
        os.path.abspath(
            r"c:\Users\hasan\OneDrive\Masaüstü\Label__Dist_12_13__winter__v2.geojson"
        )
    )[1:-1]
    url_tuple = (url, 993280764)
    label_session_table_number_of_rows = count_number_of_rows.count_rows_of_table(
        "label_session"
    )
    id_label_session_iter = itertools.count(label_session_table_number_of_rows)
    next(id_label_session_iter)

    label_table_number_of_rows = count_number_of_rows.count_rows_of_table("label")
    id_label_iter = itertools.count(label_table_number_of_rows)
    next(id_label_iter)

    label_feature_table_number_of_rows = count_number_of_rows.count_rows_of_table(
        "label_feature"
    )
    id_label_feature_iter = itertools.count(label_feature_table_number_of_rows)
    next(id_label_feature_iter)

    label_session_table_df, label_table_df, label_feature_table_df = get_data_geoJson(
        url_tuple, id_label_session_iter, id_label_iter, id_label_feature_iter
    )

    pprint.pprint(label_session_table_df)
    print("=======================================================================")
    pprint.pprint(label_table_df)
    print("=======================================================================")
    pprint.pprint(label_feature_table_df)
