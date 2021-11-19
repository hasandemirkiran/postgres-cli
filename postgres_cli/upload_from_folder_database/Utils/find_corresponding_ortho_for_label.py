import json
import geojson
import geopandas as gpd
import pprint
import rasterio
from pyproj import Transformer 
import os

def get_label_bboxes(url):
    extension = os.path.splitext(url)[1]
    with open(url) as f:
        jsonfile = geojson.load(f)

    label_bbox_list = []
    if extension == '.geojson':
        label_bbox_list = jsonfile['boxes']
    elif extension == '.json':
        for x in jsonfile:
            label_bbox_list.append((x['bbox']))
    
    if label_bbox_list[0][0] > 1000:
        new_label_bbox_list = []
        for bbox in label_bbox_list:
            temp_bbox = []
            points_tuple = ((bbox[0], bbox[1]), (bbox[2], bbox[3]))
            transformer = Transformer.from_crs(3857, 4326)
            for pt in transformer.itransform(points_tuple):
                temp_bbox.append(pt[1])
                temp_bbox.append(pt[0])
            new_label_bbox_list.append(temp_bbox)
        return new_label_bbox_list
    return label_bbox_list

def compare_one_label_one_ortho_file(raster_bounds, label_bbox_list, url):
    # print('raster_bounds ', raster_bounds)
    total_bboxs = len(label_bbox_list)
    verified = 0
    for bbox in label_bbox_list:
        if bbox[2]<=raster_bounds[2] and bbox[2]>=raster_bounds[0] and  bbox[3]<=raster_bounds[3] and bbox[3]>=raster_bounds[1]:
            verified += 1
    if verified == total_bboxs:
        print('All of the bounding boxes are in this raster file: ', url )
    elif verified != 0:
        print(verified, ' out of ', total_bboxs, ' tile are in this raster file: ', url)

    return verified

def find_most_matched_ortho(label_bbox_list):

    with open(r"Utils\ortho_url_bounds_dict.txt") as f:
        data = f.read()
    ortho_url_bounds_dict = json.loads(data)
    ortho_verified_dict = {}
    for url in ortho_url_bounds_dict:
        raster_bounds = ortho_url_bounds_dict[url]
        verified = compare_one_label_one_ortho_file(raster_bounds, label_bbox_list, url)
        ortho_verified_dict[url] = verified
    
    return ortho_verified_dict

        

if __name__ == "__main__":

    label_url = r'c:\Users\hasan\OneDrive\Masaüstü\Label__Dist_12_13__winter__v2.geojson'
    label_bbox_list = get_label_bboxes(label_url)

    ortho_verified_dict = find_most_matched_ortho(label_bbox_list)
    max_verified_tuple = [0,0]
    for url in ortho_verified_dict:
        if ortho_verified_dict[url] > max_verified_tuple[1]:
            max_verified_tuple[0] = url
            max_verified_tuple[1] = ortho_verified_dict[url]
    print(max_verified_tuple)

