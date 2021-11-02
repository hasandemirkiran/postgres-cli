import json
import geojson    
import numpy as np   

# compare 2 files if the label areas overlap or not 
def compare_2_files(URL_1, URL_2):
    tile_list_1 = []
    tile_list_2 = []

    with open(URL_1) as json_file:
        data = json.load(json_file)
        for feature_collection in data:
            temp_tile = feature_collection['properties']['tile']
            tile_list_1.append(temp_tile)

    with open(URL_2) as json_file:
        data = json.load(json_file)
        for feature_collection in data:
            temp_tile = feature_collection['properties']['tile']
            tile_list_2.append(temp_tile)

    counter_1 = 0
    for tile in tile_list_1:
        if tile not in tile_list_2:
            counter_1 += 1 

    counter_2 = 0
    for tile in tile_list_2:
        if tile not in tile_list_1:
            counter_2 += 1 
    
    if counter_1 == 0 and counter_2 == 0:
        print ('They are the same files.')
    elif counter_1 != 0 and counter_2 == 0 :
        print ('First file is the more inclusive.')
    elif counter_2 != 0 and counter_1 == 0:
        print ('Second file is the more inclusive.')
    else:
        if counter_1 == len(tile_list_1) and counter_2 == len(tile_list_2):
            print ('They are completely different files.')
        else:
            print ('They are different files but there is an intersection.')  



if __name__ == "__main__":
    URL_1 = ''
    URL_2 = ''
    compare_2_files(URL_1,URL_2)
