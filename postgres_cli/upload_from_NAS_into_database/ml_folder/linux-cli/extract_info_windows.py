import geopandas as gpd
import rasterio
import fiona
import uuid
import pandas as pd
import pprint
from pyproj import Transformer
import geojson
from shapely.geometry import Polygon, Point, box
from sqlalchemy import *
from sqlalchemy.sql.expression import label
import json
import itertools


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

    with open(url) as f:
        data = json.load(f)
    json_df = pd.json_normalize(data)

    # --- label_session table entries ---
    label_session_table_id = []
    label_session_table_id.append(next(id_label_session_iter))
    label_session_table_raster_info_id = []
    label_session_table_raster_info_id.append(url_tuple[1])
    label_session_table_name = []
    name = url.split("/")[-1].split("_")[1]
    label_session_table_name.append(name)
    label_session_table_df = gpd.GeoDataFrame(
        list(
            zip(
                label_session_table_id,
                label_session_table_name,
                label_session_table_raster_info_id,
            )
        ),
        columns=["id", "name", "raster_info_id"],
    )

    # --- label table entries ---
    num_of_bbox = len(json_df["bbox"])
    label_table_id = [next(id_label_iter) for x in range(num_of_bbox)]
    label_table_session_id = [label_session_table_id[0] for x in range(num_of_bbox)]

    label_table_label_area_EPSG4326 = json_df["bbox"]

    # copy label_area_list to use in the label_feature table
    label_table_label_area_EPSG4326_copy = (
        label_table_label_area_EPSG4326.values.tolist()
    )

    label_table_label_area_EPSG3857 = []
    transformer = Transformer.from_crs(4326, 3857)
    for x in label_table_label_area_EPSG4326:
        points_tuple = ((x[0], x[1]), (x[2], x[3]))
        point_to_add = []
        for pt in transformer.itransform(points_tuple):
            point_to_add.append(pt[0])
            point_to_add.append(pt[1])
        label_table_label_area_EPSG3857.append(point_to_add)
    label_table_label_area_EPSG4326 = [
        box(x[0], x[2], x[1], x[3]) for x in label_table_label_area_EPSG4326
    ]
    label_table_label_area_EPSG3857 = [
        box(x[0], x[2], x[1], x[3]) for x in label_table_label_area_EPSG3857
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
        list_geom.append(row["geom_EPSG4326"])

    # ---label_feature table ---
    label_feature_class_list = []
    label_feature_feature_area_list = []
    label_feature_bbox_list = []
    for feature_collection in data:
        for feature in feature_collection["features"]:
            if feature_collection["bbox"] in json_df["bbox"].tolist():
                label_feature_bbox_list.append(feature_collection["bbox"])
                label_feature_class_list.append(feature["properties"]["class"])
                label_feature_feature_area_list.append(
                    feature["geometry"]["coordinates"]
                )

    label_feature_table_id = [
        next(id_label_feature_iter) for x in range(len(label_feature_class_list))
    ]
    label_feature_table_label_id = [
        list_id[label_table_label_area_EPSG4326_copy.index(bbox_4326)]
        for bbox_4326 in label_feature_bbox_list
    ]
    label_feature_table_feature_area = [
        Point(x[0], x[1]) for x in label_feature_feature_area_list
    ]
    label_feature_table_class_id = [class_dict[x] for x in label_feature_class_list]
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


def pick_all_geojson():

    label_last_list = [
        # ('\\\\192.168.37.4\\ml\\datasets\\forestry\\Bahn\\examined_labels_v1.json', ), # We probably don't want to upload this file - Chris
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Baumbach\\label_Baumbach_class_and_center_Christian_v2.json",
            643570190,
        ),
        # ('\\\\192.168.37.4\\ml\\datasets\\forestry\\CenterForst_Magdeburg\\center_label_v1__class_label_v2__merged__Hasan.json', ), # intersection with the below one # NO ORTHO
        # ('\\\\192.168.37.4\\ml\\datasets\\forestry\\Freiburg\\subset_labels_24_03.json', ),  NO ORTHO
        # ('\\\\192.168.37.4\\ml\\datasets\\forestry\\Fremdingen\\labels_no_bad_quality.json', ), NO ORTHO
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Fugger\\label_Wellenburg_David_Christian_merged_Hasan_v1__merged__david_label_v2__Hasan.json",
            865897005,
        ),  # I have merged these 3 files
        (
            "\\\\192.168.37.4\\ml\datasets\\forestry\\Hofos\\Fienerode\\label_for_class_v1_v2_v3_center_merged_Hasan.json",
            1549623786,
        ),  # I have merged these 4 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Hofos\\Hellwig\\david_label_v2.json",
            368718515,
        ),
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Hofos\\Hellwig\\hellwig_david_label_v1.json",
            368718515,
        ),
        # ('\\\\192.168.37.4\\ml\\datasets\\forestry\\MagdeburgAlpha\\labels_no_bad_quality.json', ), NO ORTHO
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen\\Meyerei_371_384__splitted__lables_from_qgis_14_02_20_v2_merged_Hasan.json",
            1594439059,
        ),  # I have merged and splitted these files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen\\Engelbertswald_151_164__splitted__lables_from_qgis_14_02_20_v2_merged_Hasan.json",
            1219833925,
        ),  # I have merged and splitted these files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen\\Eleonorenwald_Merged__splitted__lables_from_qgis_14_02_20_v2_merged_Hasan.json",
            492843671,
        ),  # I have merged and splitted these files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Meyerei_431_435__splitted____Hasan.json",
            814970607,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Meyerei_441_442__splitted____Hasan.json",
            545542893,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Meyerei_461_471__splitted____Hasan.json",
            1502837897,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Eleonorenwald_851_857__splitted____Hasan.json",
            538906045,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Engelbertswald_101_106__splitted____Hasan.json",
            613552769,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Engelbertswald_121_125__splitted____Hasan.json",
            1483049665,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Engelbertswald_131__splitted____Hasan.json",
            1351175135,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Engelbertswald_141_142__splitted____Hasan.json",
            24481145,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Engelbertswald_171_173__splitted____Hasan.json",
            1177583935,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Engelbertswald_220_230__splitted____Hasan.json",
            445247204,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory\\label_Meppen_v1__ortho__Hedwigenwald_611_626__splitted____Hasan.json",
            504662898,
        ),  # I have splitted into 11 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\MeppenInventurV2\\label_inventory_elenorenwald\\elenorenwald_label_v1_and_v2_and_not_trees_v1_and_v3.json",
            1361376792,
        ),
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen_2\\Eleonorenwald\\label\\label_v1.json",
            492843671,
        ),
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen_3\\label\\labels_v1__ortho__Meyerei_341__splitted____Hasan.json",
            1873013021,
        ),  # I have splitted into 3 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen_3\\label\\labels_v1__ortho__Meyerei_501_506__splitted____Hasan.json",
            1773769946,
        ),  # I have splitted into 3 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen_3\\label\\labels_v1__ortho__Meyerei_511_513__splitted____Hasan.json",
            1153122822,
        ),  # I have splitted into 3 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen_Center\\center-label-extra-DOPs__ortho__Hedwigenwald_601__splitted____Hasan.json",
            22563438,
        ),  # I have splitted these files into 3
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen_Center\\center-label-extra-DOPs__ortho__Meyerei_351_354__splitted____Hasan.json",
            231527044,
        ),  # I have splitted these files into 3
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen_Center\\center-label-extra-DOPs__ortho__Engelbertswald_101_106__splitted____Hasan.json",
            613552769,
        ),  # I have splitted these files into 3
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen_Center\\center_label_felix_v1__merged__Eleonorenwald_801_836__splitted__lables_from_qgis_14_02_20_v2_merged_Hasan.json",
            1361376792,
        ),  # I have merged a non-splitted and a merged-and-splitted file
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Toering\\labels_v1_plus_v2__ortho__Gutenzell-0__splitted__Hasan.json",
            241077077,
        ),  # I have splitted these 2 files
        (
            "\\\\192.168.37.4\\ml\\datasets\\forestry\\Toering\\labels_v1_plus_v2__ortho__Gutenzell-1__splitted__Hasan.json",
            588133272,
        ),
    ]

    id_label_session_iter = itertools.count(21)
    next(id_label_session_iter)

    id_label_iter = itertools.count(1030)
    next(id_label_iter)

    id_label_feature_iter = itertools.count(41435)
    next(id_label_feature_iter)

    label_df_list = []
    for url_tuple in label_last_list:
        (
            label_session_table_df,
            label_table_df,
            label_feature_table_df,
        ) = get_data_geoJson(
            url_tuple, id_label_session_iter, id_label_iter, id_label_feature_iter
        )
        label_df_list.append(
            (label_session_table_df, label_table_df, label_feature_table_df)
        )

    return label_df_list


if __name__ == "__main__":
    label_df_list = pick_all_geojson()
    pprint.pprint(label_df_list)
