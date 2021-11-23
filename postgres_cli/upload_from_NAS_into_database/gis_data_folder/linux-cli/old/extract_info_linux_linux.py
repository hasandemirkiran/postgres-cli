import geopandas as gpd
import rasterio
import fiona
import hashlib
import shortuuid
import uuid
import pandas as pd
import pprint
from pyproj import Transformer
import geojson
from shapely.geometry import Polygon, Point, box
from sqlalchemy import *


def get_data_geoJson(url):

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
    label_session_table_id.append(uuid.uuid4().int & (1 << 31) - 1)
    label_session_table_session_area = []
    b = box(
        geojson_gpd.total_bounds.tolist()[0],
        geojson_gpd.total_bounds.tolist()[2],
        geojson_gpd.total_bounds.tolist()[1],
        geojson_gpd.total_bounds.tolist()[3],
    )
    label_session_table_session_area.append(b)
    label_session_table_raster_info_id = []
    label_session_table_raster_info_id.append(raster_info_id)
    label_session_table_df = gpd.GeoDataFrame(
        list(
            zip(
                label_session_table_id,
                label_session_table_session_area,
                label_session_table_raster_info_id,
            )
        ),
        columns=["id", "geom", "raster_info_id"],
    )

    # --- label table entries ---
    num_of_bbox = geojson_gpd.bbox_id.values.max() + 1
    label_table_id = [uuid.uuid4().int & (1 << 31) - 1 for x in range(num_of_bbox)]
    label_table_session_id = [label_session_table_id[0] for x in range(num_of_bbox)]
    label_bbox_ids = geojson_gpd.loc[:, "bbox_id"]

    with open(url) as f:
        geojson_gpd_2 = geojson.load(f)
    # label_table_label_area = [x['bbox'] for x in geojson_gpd_2['features']]
    label_table_label_area_EPSG3857 = geojson_gpd_2["boxes"]
    # label_table_label_area = []
    # for x in label_bbox_ids:
    #     current_bbox = bbox_list[x]
    #     label_table_label_area.append()
    # convert bbox from epsg:3857 to epsg:4326
    label_table_label_area_EPSG4326 = []
    transformer = Transformer.from_crs(3857, 4326)
    # print(label_table_label_area_EPSG3857)
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
        uuid.uuid4().int & (1 << 31) - 1 for x in range(len(label_feature_class))
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


# Function to pick necessary data from ortho_last
def pick_from_ortho_dict(ortho_last):
    ortho_list_to_upload = []

    for customer in ortho_last:
        for region in ortho_last[customer]:
            for url in list(ortho_last[customer][region]):
                x = url.split("/")
                y = x[-1].split("__")
                region_part = y[1]
                if len(y) == 5 and y[-1] != "CIR.gpkg":
                    gsd = y[2]
                    resolution = y[3]
                    date = y[4].split(".")[0]
                else:
                    if int(y[2][:-2]) < 100:
                        gsd = y[2]
                        resolution = -1
                    else:
                        gsd = -1
                        resolution = y[2]

                    date = y[3].split(".")[0]
                extn = x[-1].split(".")[-1]

                info = {
                    "customer": customer,
                    "region": region,
                    "region_part": region_part,
                    "gsd": gsd,
                    "resolution": resolution,
                    "date": date,
                    "url": url,
                    "extn": extn,
                }
                ortho_list_to_upload.append(info)

    id = [uuid.uuid4().int & (1 << 31) - 1 for x in range(len(ortho_list_to_upload))]
    ortho_df = pd.DataFrame(ortho_list_to_upload)
    ortho_df.insert(0, "id", id)

    return ortho_df


def pick_from_label_dict():
    picked_label_last = {
        "Blauwald": {
            "Duttenstein": [
                (
                    "/Volumes/gis_data/customers/Blauwald/Duttenstein/image_processing_data/labels/Label__Duttenstein__david__v1.geojson",
                    1191611081,
                ),
                (
                    "/Volumes/gis_data/customers/Blauwald/Duttenstein/image_processing_data/labels/Label__Duttenstein__felix__v1.geojson",
                    1191611081,
                ),
                (
                    "/Volumes/gis_data/customers/Blauwald/Duttenstein/image_processing_data/labels/Label__Duttenstein__sarah__v1.geojson",
                    1191611081,
                ),
            ]
        },
        "Fugger": {
            "Wellenburg": [
                (
                    "/Volumes/gis_data/customers/Fugger/Wellenburg/image_processing_data/labels/Label__Wellenburg__incl_fir__v2.geojson",
                    570089765,
                )
            ]
        },
        "GrafSpreti": {
            "Lotzbeck": [
                (
                    "/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/image_processing_data/labels/Label__Lotzbeck_1__luca__v1.geojson",
                    603067098,
                ),
                (
                    "/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/image_processing_data/labels/Label__Lotzbeck_4__hasan__v1.geojson",
                    547899782,
                ),
            ]
        },
        "ToeringJettenbach": {
            "Jettenbach": [
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_12__2021_08_02-07_19_122__v3.geojson",
                    1017474306,
                ),
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_14__54mm__867mm__2021_08_24-11_47_48__v2.geojson",
                    1551163119,
                ),
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_1__2021_08_02-07_21_17__v2.geojson",
                    1354782117,
                ),
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_3__2021_08_02-07_18_55__v3.geojson",
                    53041937,
                ),
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_5__58mm__932mm__2021_08_24-11_45_44__v2.geojson",
                    709293274,
                ),
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_7__58mm__932mm__2021_08_24-11_46_49__v2.geojson",
                    424785541,
                ),
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_8__2021_08_04-08_51_43__v2.geojson",
                    1358770326,
                ),
            ],
            "Winhoering": [
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_1____v4.geojson",
                    815001220,
                ),
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_2____v4.geojson",
                    2099520860,
                ),
                (
                    "/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_3____v4.geojson",
                    1539914621,
                ),
            ],
        },
        "VonPfuel": {
            "Tuessling": [
                (
                    "/Volumes/gis_data/customers/VonPfuel/Tuessling/image_processing_data/labels/Label__Tuessling_1__Christian__v3.geojson",
                    1810882877,
                )
            ]
        },
        "Wallerstein": {
            "Dist_12_13": [
                (
                    "/Volumes/gis_data/customers/Wallerstein/Dist_12_13/image_processing_data/labels/Label__Dist_12_13__winter__v2.geojson",
                    1293779069,
                )
            ]
        },
    }
    return picked_label_last


def get_data_geoJson_all():
    geojson_cluster = []
    picked_label_last = pick_from_label_dict()
    for customer in picked_label_last:
        for region in picked_label_last[customer]:
            for url_tuple in picked_label_last[customer][region]:
                if url_tuple != []:
                    print(url_tuple)
                    (
                        label_session_table_df,
                        label_table_df,
                        label_feature_table_df,
                    ) = get_data_geoJson(url_tuple)
                    geojson_cluster.append(
                        [label_session_table_df, label_table_df, label_feature_table_df]
                    )

    return geojson_cluster


print(get_data_geoJson_all())
