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

    with open(r'label_Wellenburg_David_Christian_merged_Hasan_v1__merged__david_label_v2__Hasan.json', 'w') as convert_file:
        convert_file.write(json.dumps(data))

if __name__ == "__main__":
    URL_1 = '\\\\192.168.37.4\\ml\\datasets\\forestry\\Fugger\\label_Wellenburg_David_Christian_merged_Hasan_v1.json'
    URL_2 = '\\\\192.168.37.4\\ml\\datasets\\forestry\\Wellenburg\\david_label_v2.json'
    merge_2_files(URL_1,URL_2)
