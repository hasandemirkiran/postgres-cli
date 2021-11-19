# 32  out of  158  tile are in this raster file:  \\192.168.37.4\gis_data\customers\ArenbergMeppen\Eleonorenwald\raster\Orthos\Ortho__Eleonorenwald_801_836__75mm__1200mm__2020_06_24.gpkg
# 1  out of  158  tile are in this raster file:  \\192.168.37.4\gis_data\customers\ArenbergMeppen\Eleonorenwald\raster\Orthos\Ortho__Eleonorenwald_851_857__80mm__1280mm__2020_06_24.gpkg
# 82  out of  158  tile are in this raster file:  \\192.168.37.4\gis_data\customers\ArenbergMeppen\Engelbertswald\raster\Orthos\Ortho__Engelbertswald_151_164__65mm__1005mm__2020_08_06.gpkg
# 82  out of  158  tile are in this raster file:  \\192.168.37.4\gis_data\customers\ArenbergMeppen\Engelbertswald\raster\Orthos\Ortho__Engelbertswald_151_164__65mm__262mm__2020_08_06.gpkg
# 3  out of  158  tile are in this raster file:  \\192.168.37.4\gis_data\customers\ArenbergMeppen\Hedwigenwald\raster\Orthos\Ortho__Hedwigenwald_711_720__80mm__1280mm__2020_06_24.gpkg
# 26  out of  158  tile are in this raster file:  \\192.168.37.4\gis_data\customers\ArenbergMeppen\Karlswald\raster\Orthos\Ortho__Meyerei_371_384__65mm__1004mm__2020_08_06.gpkg
# 26  out of  158  tile are in this raster file:  \\192.168.37.4\gis_data\customers\ArenbergMeppen\Karlswald\raster\Orthos\Ortho__Meyerei_371_384__65mm__261mm__2020_08_06.gpkg
# 47  out of  158  tile are in this raster file:  \\192.168.37.4\gis_data\customers\ArenbergMeppen\Eleonorenwald\raster\Orthos\Ortho__Eleonorenwald_Merged__2020_06_24.tif
# ['\\\\192.168.37.4\\gis_data\\customers\\ArenbergMeppen\\Engelbertswald\\raster\\Orthos\\Ortho__Engelbertswald_151_164__65mm__1005mm__2020_08_06.gpkg', 82]

import json
import find_corresponding_ortho_for_label
import pprint


def find_orthoURL_of_bbox(bbox, ortho_url_bounds_dict):
    for url in ortho_url_bounds_dict:
        ortho_bounds = ortho_url_bounds_dict[url]
        if (
            bbox[2] <= ortho_bounds[2]
            and bbox[2] >= ortho_bounds[0]
            and bbox[3] <= ortho_bounds[3]
            and bbox[3] >= ortho_bounds[1]
        ):
            return url


def split_label(label_URL):
    label_bbox_ortho_dict = {}
    ortho_url_bounds_dict_url = (
        r"c:\Users\hasan\OneDrive\Masaüstü\postgres-cli\Utils\ortho_url_bounds_dict.txt"
    )

    with open(ortho_url_bounds_dict_url) as dict_file:
        ortho_url_bounds_dict = json.load(dict_file)

    with open(label_URL) as f:
        label_json = json.load(f)

    label_bboxes = find_corresponding_ortho_for_label.get_label_bboxes(label_URL)
    print("Number of label bboxes: ", len(label_bboxes))
    for feature_collection in label_json:
        bbox = feature_collection["bbox"]
        url = find_orthoURL_of_bbox(bbox, ortho_url_bounds_dict)
        if url != None:
            if url not in label_bbox_ortho_dict:
                label_bbox_ortho_dict[url] = []
            label_bbox_ortho_dict[url].append(feature_collection)

    return label_bbox_ortho_dict


def create_splitted_files(label_bbox_ortho_dict, label_name):

    for url in label_bbox_ortho_dict:
        ortho_name = url.split("\\")[-1].split("__")[1]

        with open(
            label_name + "__ortho__" + ortho_name + "__splitted" + "__Hasan.json", "w"
        ) as convert_file:
            convert_file.write(json.dumps(label_bbox_ortho_dict[url]))


if __name__ == "__main__":
    label_URL = (
        "\\\\192.168.37.4\\ml\\datasets\\forestry\\Toering\\labels_v1_plus_v2.json"
    )
    label_name = "labels_v1_plus_v2"
    label_bbox_ortho_dict = split_label(label_URL)
    create_splitted_files(label_bbox_ortho_dict, label_name)
