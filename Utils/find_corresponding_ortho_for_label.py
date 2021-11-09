import json
import geojson
import geopandas as gpd
import pprint
import rasterio
from pyproj import Transformer 

def get_label_bboxes(url):
    with open(url) as f:
        jsonfile = geojson.load(f)
    label_bbox_list = []
    for x in jsonfile:
        label_bbox_list.append((x['bbox']))
        # print(x['bbox'])
    return label_bbox_list

def get_raster_bounds(url):
    raster = rasterio.open(url)
    raster_bounding_box = raster.bounds
    raster_format = raster.crs
    raster_bounds = []

    if raster_format != 'EPSG:4326':
        points_tuple = ((raster_bounding_box[0], raster_bounding_box[1]), (raster_bounding_box[2], raster_bounding_box[3]))
        transformer = Transformer.from_crs(3857, 4326)
        for pt in transformer.itransform(points_tuple):
            raster_bounds.append(pt[1])
            raster_bounds.append(pt[0])
    else:
        raster_bounds.append(raster_bounding_box[0])
        raster_bounds.append(raster_bounding_box[1])
        raster_bounds.append(raster_bounding_box[2])
        raster_bounds.append(raster_bounding_box[3])
    print(raster_bounds)
    return raster_bounds


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
    # ortho_url = '\\\\192.168.37.4\\gis_data\\customers\\ArenbergMeppen\\Eleonorenwald\\raster\\Orthos\\Ortho__Eleonorenwald_Merged__2020_06_24.tif'
    # raster_bounds = get_raster_bounds(ortho_url)
    # print(raster_bounds)

    label_url = '\\\\192.168.37.4\\ml\\datasets\\forestry\\CenterForst_Magdeburg\\class_label_v2.json'
    label_bbox_list = get_label_bboxes(label_url )

    # compare_one_label_one_ortho_file(raster_bounds, label_bbox_list)
    ortho_verified_dict = find_most_matched_ortho(label_bbox_list)
    max_verified_tuple = [0,0]
    for url in ortho_verified_dict:
        if ortho_verified_dict[url] > max_verified_tuple[1]:
            max_verified_tuple[0] = url
            max_verified_tuple[1] = ortho_verified_dict[url]
    print(max_verified_tuple)

