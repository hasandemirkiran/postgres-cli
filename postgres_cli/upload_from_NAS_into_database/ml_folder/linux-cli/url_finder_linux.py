import os
import re
import pprint


def find_URLs(start_path):

    label_url_list = []

    for root, dirs, files in os.walk(start_path):
        if (
            "images" not in root
            and "xyz" not in root
            and "comparison-images-labels" not in root
            and "Export" not in root
        ):
            for f in files:
                # There is not any Ortho file in ml folder that is why only check label files
                if ("label" or "Label") in f and f.endswith(".json"):
                    url = root + "/" + f
                    x = url.split("/")
                    if x[-2] == "Decreapted" or x[-3] == "Decreapted":
                        continue
                    label_url_list.append(url)
                # file is not label
                else:
                    pass
    return label_url_list


if __name__ == "__main__":
    path = "/"

    label_url_list = find_URLs(path)

    pprint.pprint(label_url_list)
