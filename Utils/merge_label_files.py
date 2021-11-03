import json

def merge_2_files(URL_1, URL_2):

    data = []
    sum_tile_list = []
    
    with open(URL_1) as json_file:
        json_data = json.load(json_file)
        for feature_collection in json_data:
            temp_tile = feature_collection['properties']['tile']
            if temp_tile not in sum_tile_list:
                sum_tile_list.append(temp_tile)
                data.append(feature_collection)
            else:
                pass

    with open(URL_2) as json_file:
        json_data = json.load(json_file)
        for feature_collection in json_data:
            temp_tile = feature_collection['properties']['tile']
            if temp_tile not in sum_tile_list:
                sum_tile_list.append(temp_tile)
                data.append(feature_collection)
            else:
                pass

    with open(r'labels_no_bad_quality_and_labels_from_qgis_elenoren_only_merged_Hasan.json', 'w') as convert_file:
        convert_file.write(json.dumps(data))

if __name__ == "__main__":
    URL_1 = '\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen\\labels_no_bad_quality.json'
    URL_2 = '\\\\192.168.37.4\\ml\\datasets\\forestry\\Meppen\\labels_from_qgis_elenoren_only.json'
    merge_2_files(URL_1,URL_2)
