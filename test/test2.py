import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point, box
from shapely.geometry.linestring import LineString

# print(type([12.542811636363634, 48.50293363636363, 12.553058, 48.51191581818186]))
# print(type(box(12.542811636363634, 48.50293363636363, 12.553058, 48.51191581818186)))


def normalize_bbox(bbox):
    def swap(i_a, i_b):
        tmp = bbox[i_a]
        bbox[i_a] = bbox[i_b]
        bbox[i_b] = tmp
    def fix_order(i_a, i_b):
        if bbox[i_a] > bbox[i_b]:
            swap(i_a, i_b)
    fix_order(0, 2)
    fix_order(1, 3)
    return bbox

print(normalize_bbox([12.553058,48.50293363636363,  48.51191581818186, 12.542811636363634,]))