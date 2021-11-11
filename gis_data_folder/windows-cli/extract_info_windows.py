import geopandas as gpd
import rasterio
import fiona
import shortuuid
import uuid
import pandas as pd
import pprint
from pyproj import Transformer
import geojson
from shapely.geometry import Polygon, Point, box
from sqlalchemy import *
from sqlalchemy.sql.expression import label
import itertools



def get_data_geoJson(url_tuple, id_label_session_iter, id_label_iter, id_label_feature_iter):

    url = url_tuple[0]
    
    class_dict = {'Douglas': 0, 'Fir': 1, 'Larch': 2, 'Spruce': 3, 'Pine': 4, 'Leaved Tree': 5, 'Dead Tree': 6, 'Young Tree': 7, 'Background': 8, 'Unknown': 9, 'done': 10, 'Dead Pine': 11, 'Douglas fir': 12, 'healthy': 13, 'dead': 14, 'affected': 15, 'no class': 16}  

    geojson_gpd = gpd.read_file(url)

    # --- label_session table entries ---
    label_session_table_id = []
    label_session_table_id.append(next(id_label_session_iter))
    label_session_table_session_area = []
    b = box(geojson_gpd.total_bounds.tolist()[0], geojson_gpd.total_bounds.tolist()[2], geojson_gpd.total_bounds.tolist()[1], geojson_gpd.total_bounds.tolist()[3])
    label_session_table_session_area.append(b)
    label_session_table_raster_info_id = []
    label_session_table_raster_info_id.append(url_tuple[1])
    label_session_table_name = []
    name = url.split(r'\\')[-1].split('__')[1]
    label_session_table_name.append(name)

    label_session_table_df = gpd.GeoDataFrame(list(zip(label_session_table_id, label_session_table_name, label_session_table_session_area, label_session_table_raster_info_id)), columns =['id','name', 'geom', 'raster_info_id'])

    # --- label table entries ---
    num_of_bbox = geojson_gpd.bbox_id.values.max() + 1
    label_table_id = [next(id_label_iter) for x in range(num_of_bbox)]
    label_table_session_id = [label_session_table_id[0] for x in range(num_of_bbox)]

    with open(url) as f:
        geojson_gpd_2 = geojson.load(f)
    label_table_label_area_EPSG3857 = geojson_gpd_2['boxes']
    label_table_label_area_EPSG4326 = []
    transformer = Transformer.from_crs(3857, 4326)
    for x in label_table_label_area_EPSG3857:
        points_tuple = ((x[0], x[1]), (x[2], x[3]))
        point_to_add = []
        for pt in transformer.itransform(points_tuple):
            point_to_add.append(pt[0])
            point_to_add.append(pt[1])
        label_table_label_area_EPSG4326.append(point_to_add)


    label_table_label_area_EPSG3857 = [box(x[0],x[2],x[1],x[3]) for x in label_table_label_area_EPSG3857]
    label_table_label_area_EPSG4326 = [box(x[0],x[2],x[1],x[3]) for x in label_table_label_area_EPSG4326]
    label_table_df = gpd.GeoDataFrame(list(zip(label_table_id, label_table_session_id,label_table_label_area_EPSG4326, label_table_label_area_EPSG3857)), columns =['id', 'session_id', 'geom_EPSG4326', 'geom_EPSG3857'])

    # dict to use in label_feature table while finding the label_feature_table_label_id
    list_id = []
    list_geom = []
    for index, row in label_table_df.iterrows():
        list_id.append(row['id'])
        list_geom.append(row['geom_EPSG3857'])
    # fetch a row with a value from label_table_df
    # print(label_table_df.loc[label_table_df.label_area_EPSG3857.apply(lambda x: x == [1396989.2801922676, 6191713.417884247, 1397035.0114690675,6191759.284482648])])

    # ---label_feature table ---
    label_feature_class = geojson_gpd.loc[:, 'class']

    label_feature_table_id = [next(id_label_feature_iter) for x in range(len(label_feature_class))]

    label_features_bbox_id= geojson_gpd.loc[:, 'bbox_id']
    label_features_bbox_EPSG3857 = [label_table_label_area_EPSG3857[x] for x in label_features_bbox_id]
    label_feature_table_label_id = [list_id[list_geom.index(geom)] for geom in label_features_bbox_EPSG3857]

    label_feature_table_feature_area = geojson_gpd.loc[:, 'geometry']
    label_feature_table_class_id = [class_dict[x] for x in label_feature_class]
    label_feature_table_df = gpd.GeoDataFrame(list(zip(label_feature_table_id, label_feature_table_label_id,label_feature_table_feature_area, label_feature_table_class_id)), columns =['id', 'label_id', 'geom', 'class_id'])

    return (label_session_table_df, label_table_df, label_feature_table_df)

    # gpd.GeoDataFrame({'id': id, 'class_id': class_series_ids,'geom':  feature_area_series,'label_id': bbox_id_series})


# Function to pick necessary data from ortho_last
def pick_from_ortho_dict(ortho_last):
    ortho_list_to_upload = []

    for customer in ortho_last:
        for region in ortho_last[customer]:
            for url in list(ortho_last[customer][region]):
                x = url.split('\\')
                y = x[-1].split('__')
                region_part = y[1]
                if len(y) == 5 and y[-1] != 'CIR.gpkg':
                    gsd = y[2]
                    resolution = y[3]
                    date = y[4].split('.')[0]
                else:
                    if int(y[2][:-2]) < 100:
                        gsd = y[2]
                        resolution = -1
                    else:
                        gsd = -1
                        resolution = y[2]

                    date = y[3].split('.')[0]
                extn = x[-1].split('.')[-1]

                info = {
                    'customer' : customer, 
                    'region' : region,
                    'region_part' : region_part,
                    'gsd' : gsd,
                    'resolution' : resolution,
                    'date' : date,
                    'url': url,
                    'extn' : extn
                }
                ortho_list_to_upload.append(info)

    id = [uuid.uuid4().int & (1<<31)-1 for x in range(len(ortho_list_to_upload))]
    ortho_df = pd.DataFrame(ortho_list_to_upload)
    ortho_df.insert(0, 'id', id)

                
    return ortho_df


def pick_all_geojson():
    label_last= {
          'ArenbergMeppen': {
              'Engelbertswald': [('\\\\192.168.37.4\\gis_data\\customers\\ArenbergMeppen\\Engelbertswald\\image_processing_data\\labels\\Label__ArenbergMeppen__Engelbertswald__2021_10_26__Hasan__v1_TRAININGLABELS.geojson', 1442470281)]},  
        'Blauwald': {
        'Duttenstein':     [('\\\\192.168.37.4\\gis_data\\customers\\Blauwald\\Duttenstein\\image_processing_data\\labels\\Label__Duttenstein__david__v1.geojson', 1514098108),
                            ('\\\\192.168.37.4\\gis_data\\customers\\Blauwald\\Duttenstein\\image_processing_data\\labels\\Label__Duttenstein__felix__v1.geojson', 1514098108),
                            ('\\\\192.168.37.4\\gis_data\\customers\\Blauwald\\Duttenstein\\image_processing_data\\labels\\Label__Duttenstein__sarah__v1.geojson', 1514098108)]},
        'CenterForst': {
            'Immergruen':   [('\\\\192.168.37.4\\gis_data\\customers\\CenterForst\\Immergruen\\image_processing_data\\labels\\Label__Immergruen__felix__fixed__v1.geojson', 542896300)]},
        'Fugger': {
            'Wellenburg':   [('\\\\192.168.37.4\\gis_data\\customers\\Fugger\\Wellenburg\\image_processing_data\\labels\\Label__Wellenburg__incl_fir__v2.geojson', 865897005)]},
        'GrafSpreti': {
            'Lotzbeck':     [('\\\\192.168.37.4\\gis_data\\customers\\GrafSpreti\\Lotzbeck\\image_processing_data\\labels\\Label__Lotzbeck_1__luca__v1.geojson', 1257217749),
                             ('\\\\192.168.37.4\\gis_data\\customers\\GrafSpreti\\Lotzbeck\\image_processing_data\\labels\\Label__Lotzbeck_2__luca__v1.geojson', 1417803468),
                             ('\\\\192.168.37.4\\gis_data\\customers\\GrafSpreti\\Lotzbeck\\image_processing_data\\labels\\Label__Lotzbeck_4__hasan__v2.geojson', 178416618)]},
        'HofosOldershausen': {
            'Breitenbach': [('\\\\192.168.37.4\\gis_data\\customers\\HofosOldershausen\\Breitenbach\\image_processing_data\\labels\\Label__Breitenbach__luca__v3.geojson', 274396774)]},
        'ToeringJettenbach': {
            # 'Inning':      [('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Inning\\image_processing_data\\labels\\Label__Seefeld_Inning_2_1__v2.geojson', 2102553528)], # There is no done point, we cannot convert it with the bboxes version
            'Jettenbach':  [('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Jettenbach\\image_processing_data\\labels\\Label__Jettenbach_12__2021_08_02-07_19_122__v3.geojson', 1162362491),
                            ('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Jettenbach\\image_processing_data\\labels\\Label__Jettenbach_14__54mm__867mm__2021_08_24-11_47_48__v2.geojson', 2029944054),        
                            ('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Jettenbach\\image_processing_data\\labels\\Label__Jettenbach_1__2021_08_02-07_21_17__v2.geojson', 1905420721),
                            ('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Jettenbach\\image_processing_data\\labels\\Label__Jettenbach_3__2021_08_02-07_18_55__v3.geojson', 41921502),
                            ('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Jettenbach\\image_processing_data\\labels\\Label__Jettenbach_5__58mm__932mm__2021_08_24-11_45_44__v2.geojson', 1310343500),
                            ('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Jettenbach\\image_processing_data\\labels\\Label__Jettenbach_7__58mm__932mm__2021_08_24-11_46_49__v2.geojson', 1338409446),
                            ('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Jettenbach\\image_processing_data\\labels\\Label__Jettenbach_8__2021_08_04-08_51_43__v2.geojson', 657043355)],
            # 'Mischenried': [('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Mischenried\\image_processing_data\\labels\\Label__Mischenried__v2.geojson', 840858045)], # There is no done point, we cannot convert it with the bboxes version
            'Winhoering': [('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Winhoering\\image_processing_data\\labels\\Label__Winhoering_1____v4.geojson', 1965064980),
                            ('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Winhoering\\image_processing_data\\labels\\Label__Winhoering_2____v4.geojson', 629165559),
                            ('\\\\192.168.37.4\\gis_data\\customers\\ToeringJettenbach\\Winhoering\\image_processing_data\\labels\\Label__Winhoering_3____v4.geojson', 1162882951)]},
        'VonPfuel': {
            'Tuessling':   [('\\\\192.168.37.4\\gis_data\\customers\\VonPfuel\\Tuessling\\image_processing_data\\labels\\Label__Tuessling_1__Christian__v3.geojson', 982951984)]},
        # 'Wallerstein': {
        #     'Dist_12_13': [('\\\\192.168.37.4\\gis_ data\\customers\\Wallerstein\\Dist_12_13\\image_processing_data\\labels\\Label__Dist_12_13__winter__v2.geojson', 993280764)]} # There is no done point, we cannot convert it with the bboxes version
        }

    id_label_session_iter = itertools.count()
    next(id_label_session_iter)

    id_label_iter = itertools.count()
    next(id_label_iter)

    id_label_feature_iter = itertools.count()
    next(id_label_feature_iter)


    label_df_list = []
    for customer in label_last:
        for region in label_last[customer]:
            for url_tuple in label_last[customer][region]:
                label_session_table_df, label_table_df, label_feature_table_df = get_data_geoJson(url_tuple, id_label_session_iter, id_label_iter, id_label_feature_iter)
                label_df_list.append((label_session_table_df, label_table_df, label_feature_table_df))
    
    return label_df_list


if __name__ == "__main__":
    label_df_list = pick_all_geojson()
    pprint.pprint(label_df_list)

    