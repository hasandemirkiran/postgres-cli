import os
import re
import pprint 


ortho_list_to_upload = [] 


def find_URLs(start_path):

    ortho_customer_regions = {}
    ortho_region_urls = {}
    label_customer_regions = {}
    label_region_urls = {}

    for root, dirs, files in os.walk(start_path):
        for f in files:
            # if file is in format eg.  Ortho__Jettenbach_12__62mm__995mm__2021_06_14.gpkg
            if f.startswith('Ortho__') and f.endswith('.gpkg'):
                url = root + '/' + f
                # print('Ortho file found at : ', url)

                x = re.split('/', url)
                customer = x[4]
                region = x[5]
                if region == 'raster': region = x[4]

                # customer's regions dictionary for ortho files
                if customer in ortho_customer_regions:
                    if region not in ortho_customer_regions[customer]:
                        ortho_customer_regions[customer].append(region)
                else:
                    temp_list = []
                    temp_list.append(region)
                    ortho_customer_regions[customer] = temp_list

                # urls in the regions
                if region in ortho_region_urls:
                    if url not in ortho_region_urls[region]:
                        ortho_region_urls[region].append(url)
                else:
                    temp_list = []
                    temp_list.append(url)
                    ortho_region_urls[region] = temp_list

            # if file in a format eg. Label__Jettenbach_3__2021_08_02-07_18_55__v3.geojson
            elif f.startswith('Label__') and f.endswith('.geojson'):
                url = root + '/' + f
                # print('Label file found at : ', url)

                x = re.split('/', url)
                customer = x[4]
                region = x[5]

                # customers' regions dictionary for label files
                if customer in label_customer_regions:
                    if region not in label_customer_regions[customer]:
                        label_customer_regions[customer].append(region)
                else:
                    temp_list = []
                    temp_list.append(region)
                    label_customer_regions[customer] = temp_list

                # urls in the regions
                if region in label_region_urls:
                    if url not in label_region_urls[region]:
                        label_region_urls[region].append(url)
                else:
                    temp_list = []
                    temp_list.append(url)
                    label_region_urls[region] = temp_list

            # file not label or ortho
            else:
                pass
    return  ortho_customer_regions, ortho_region_urls, label_customer_regions, label_region_urls 


# check if ortho file exist for the label file region
def check_label_customer_regions(path):

    ortho_customer_regions, ortho_region_urls, label_customer_regions, label_region_urls  =  find_URLs(path)

    for customer in label_customer_regions.copy():
        if customer not in ortho_customer_regions:
            del label_customer_regions[customer]
        else:
            for region in label_customer_regions[customer]:
                if region not in ortho_customer_regions[customer]:
                    label_customer_regions[customer].remove(region)
    return ortho_customer_regions, ortho_region_urls, label_customer_regions, label_region_urls


def create_last_dicts(path):
    ortho_last = {}
    label_last = {}
    ortho_customer_regions, ortho_region_urls, label_customer_regions, label_region_urls  =  check_label_customer_regions(path)

    for customer in ortho_customer_regions:
        ortho_last[customer] = {}
        for region in ortho_customer_regions[customer]:
            ortho_last[customer][region] = []
            ortho_last[customer][region] = (ortho_region_urls[region])

    for customer in label_customer_regions:
        label_last[customer] = {}
        for region in label_customer_regions[customer]:
            label_last[customer][region] = []
            label_last[customer][region] = (label_region_urls[region])

    return ortho_last, label_last


def last_sorted_dicts(path):
    ortho_last, label_last = create_last_dicts(path)

    for customer in ortho_last:
        for region in ortho_last[customer]:
            ortho_last[customer][region].sort()

    for customer in label_last:
        for region in label_last[customer]:
            label_last[customer][region].sort()
    
    return ortho_last, label_last
    


if __name__ == "__main__":
    path = '/Volumes/gis_data/customers/'

    ortho_last, label_last = last_sorted_dicts(path)

    pprint.pprint(ortho_last)
    print()
    print()
    pprint.pprint(label_last)

