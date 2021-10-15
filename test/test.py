import pandas as pd
import uuid
import geopandas as gpd
import pprint
import geojson
from pyproj import Transformer


url = './data/label_data/geoData.geojson'
class_dict = {'Douglas': 0, 'Fir': 1, 'Larch': 2, 'Spruce': 3, 'Pine': 4, 'Leaved Tree': 5}  

geojson_gpd = gpd.read_file(url)

# --- label_session table entries ---
label_session_table_id = []
label_session_table_id.append(uuid.uuid4().int & (1<<31)-1)
label_session_table_session_area = []
label_session_table_session_area.append(geojson_gpd.total_bounds)
label_session_table_df = pd.DataFrame(list(zip(label_session_table_id, label_session_table_session_area)), columns =['id', 'session_area'])

# --- label table entries ---
num_of_bbox = geojson_gpd.bbox_id.values.max() + 1
label_table_id = [uuid.uuid4().int & (1<<31)-1 for x in range(num_of_bbox)]
label_table_session_id = [label_session_table_id[0] for x in range(num_of_bbox)]
label_bbox_ids = geojson_gpd.loc[:, 'bbox_id']

with open(url) as f:
    geojson_gpd_2 = geojson.load(f)
# label_table_label_area = [x['bbox'] for x in geojson_gpd_2['features']]
label_table_label_area_EPSG3857 = geojson_gpd_2['boxes']
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
label_table_df = pd.DataFrame(list(zip(label_table_id, label_table_session_id,label_table_label_area_EPSG4326, label_table_label_area_EPSG3857)), columns =['id', 'session_id', 'label_area_EPSG4326', 'label_area_EPSG3857'])

# dict to use in label_feature table while finding the label_feature_table_label_id
list_id = []
list_geom = []
for index, row in label_table_df.iterrows():
    list_id.append(row['id'])
    list_geom.append(row['label_area_EPSG3857'])
# fetch a row with a value from label_table_df
# print(label_table_df.loc[label_table_df.label_area_EPSG3857.apply(lambda x: x == [1396989.2801922676, 6191713.417884247, 1397035.0114690675,6191759.284482648])])

# ---label_feature table ---
label_feature_class = geojson_gpd.loc[:, 'class']

label_feature_table_id = [uuid.uuid4().int & (1<<31)-1 for x in range(len(label_feature_class))]

label_features_bbox_id= geojson_gpd.loc[:, 'bbox_id']
label_features_bbox_EPSG3857 = [label_table_label_area_EPSG3857[x] for x in label_features_bbox_id]
label_feature_table_label_id = [list_id[list_geom.index(geom)] for geom in label_features_bbox_EPSG3857]

label_feature_table_feature_area = geojson_gpd.loc[:, 'geometry']
label_feature_table_class_id = [class_dict[x] for x in label_feature_class]
label_feature_table_df = pd.DataFrame(list(zip(label_feature_table_id, label_feature_table_label_id,label_feature_table_feature_area, label_feature_table_class_id)), columns =['id', 'label_id', 'feature_area', 'class_id'])
print(label_feature_table_df)

