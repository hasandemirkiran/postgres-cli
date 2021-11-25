import os
import argparse
import psycopg2
import pandas as pd
import datetime
from configparser import ConfigParser, Error
from geojson import Point, Feature, FeatureCollection, dump, Polygon
import json
import yaml
from copy import deepcopy

from configs.classification_problem_config import base_config
from utils import queries_file


def db_config(filename, section="postgresql"):
    """Load configurations for database connection

    Args:
        filename (str): Path of the credentials and configurations (.ini) file necessary to connect at the database.
        section (str): Analyzed section of the configuration (.ini) file. Defaults to 'postgresql'.

    Raises:
        Exception: If the required section is not present in the configuration file

    Returns:
        dict: Configuration data
    """

    # create a parser
    parser = ConfigParser()

    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )
    return db


def fetch_from_label_db(query):
    """Execute the query to fetch the data from the label database.

    Args:
        query (str): Query for the label database.

    Returns:
        pandas.DataFrame: DataFrame containing the data fetched according the query.
    """

    try:
        params = db_config(filename="configs/database.ini", section="postgresql")

        # Connect to database
        connection = psycopg2.connect(**params)
        # print("--- Label database connection was oppened ---")
        cursor = connection.cursor()

        # Execute the query
        fetched_data = pd.io.sql.read_sql(query, connection)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return None

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            # print("--- Label database connection was closed ---")
        return fetched_data


def find_bbox_bounds(coords):
    summa = []
    for i in range(len(coords)):
        summa.append(coords[i][0] + coords[i][1])
    max_index = summa.index((max(summa)))
    min_index = summa.index((min(summa)))
    return [
        coords[min_index][0],
        coords[min_index][1],
        coords[max_index][0],
        coords[max_index][1],
    ]


def label_data_creator(queried_data, out_folder):
    actual_region = None
    actual_raster = None
    for index, row in queried_data.iterrows():
        name = row["region_name"]
        if actual_region == None:
            features = []
            actual_region = name
            actual_raster = row["raster_url"]
        else:
            # Save intermediate data
            if actual_region != name:
                create_label_file(features, out_folder, actual_region)
                update_config(
                    config, os.path.join(out_folder, actual_region), actual_raster
                )
                print(
                    "--created {} with {} points".format(actual_region, len(features))
                )
                print(actual_raster)
                actual_region = name
                actual_raster = row["raster_url"]
                features = []
        tmp = json.loads(row["label_area"])
        coordinates = find_bbox_bounds(tmp["coordinates"][0])

        features.append(
            Feature(
                geometry=Point(
                    (row["feature_coordinate_x"], row["feature_coordinate_y"]),
                    precision=14,
                ),
                properties={"class": row["tree_type"], "bbox_id": row["label_id"]},
                bbox=[coordinates[0], coordinates[1], coordinates[2], coordinates[3]],
            )
        )  # Be aware, the bbox id is not the same of the original label file

        # Save final data
        if index >= queried_data.shape[0] - 1:
            create_label_file(features, out_folder, actual_region)
            update_config(
                config, os.path.join(out_folder, actual_region), actual_raster
            )
            print("--created {} with {} points".format(actual_region, len(features)))
            print("Requested data was created!")


def update_config(config, label_path, raster_path):
    config["make_label_mappings"] = {"label_path": label_path}
    config["make_dataset__list"].append(
        {
            "image_path": raster_path,
            "label_path": label_path,
            "splits": 0,
        }
    )


def create_label_file(features, out_folder, region_name):
    feature_collection = FeatureCollection(features)
    save_path = os.path.join(out_folder, region_name)
    with open("{}.geojson".format(save_path), "w") as f:
        dump(feature_collection, f)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="""Query label data""")
    parser.add_argument(
        "--query_type",
        choices=[
            "similar_conditions",
            "temporal_interval",
            "single_tree_percentage",
            "region_name",
        ],
        type=str,
        help="Type of query used for the label database.",
    )

    # single_tree_percentage parameters
    parser.add_argument(
        "--reference_tree", type=str, help="Class of tree to use as reference one"
    )
    parser.add_argument(
        "--max_percentage",
        type=int,
        default=100,
        help="Maximum percentage of the specific tree present in the bbox",
    )
    parser.add_argument(
        "--min_percentage",
        type=int,
        default=0,
        help="Minimum percentage of the specific tree present in the bbox",
    )

    # region_name parameters
    parser.add_argument("--region", type=str, help="Name of the region to analyze")

    # temporal_intrval parameters
    parser.add_argument(
        "--start_date",
        type=datetime.date.fromisoformat,
        help="Start date for the temporal search. Input format YYYY-MM-DD",
    )
    parser.add_argument(
        "--end_date",
        type=datetime.date.fromisoformat,
        help="End date for the temporal search. Input format YYYY-MM-DD",
    )

    # similar_season parameters
    # parser.add_argument("--date", type=datetime.date.fromisoformat, help="Starting date for the temporal search. Input format YYYY-MM-DD")
    parser.add_argument(
        "--days",
        default=10,
        type=int,
        help="Interval of days to analyze before and after the starting date. Input format YYYY-MM-DD",
    )
    parser.add_argument(
        "--months",
        default=0,
        type=int,
        help="Interval of months to analyze before and after the starting date. Input format YYYY-MM-DD",
    )

    # parser.add_argument("--max_cloud_presence", type=float, help="Maximum level of cloud presence in the scene")
    # parser.add_argument("--min_cloud_presence", type=float, help="Minimum level of cloud presence in the scene")

    # parser.add_argument("--starting_date", type=datetime.date.fromisoformat, help="Starting date for the temporal search. Input format YYYY-MM-DD hh:mm")

    parser.add_argument("--output_path", type=str, help="Path for the output file")

    args = parser.parse_args()

    try:
        # Fetch data
        df = fetch_from_label_db(
            "SELECT id AS id, name AS name FROM public.tree_class;"
        )
        tree_types = df.set_index("name").to_dict()["id"]
    except Exception as error:
        print("Error in the tree classes data fetching", error)
        quit()

    # Create output folder
    now = datetime.datetime.now()
    current_time = now.strftime("%Y_%m_%d-%H_%M_%S")
    out_folder = os.path.join(
        args.output_path, "training_data_{}/".format(current_time)
    )
    os.mkdir(out_folder)

    ### Prepare the config file
    config = deepcopy(base_config)
    config["Albunet"]["dropout"] = 0.0
    config["make_loader"]["batch_size"] = 8
    config["do_training"]["job_name"] = "classification"
    config["do_training"]["epochs"] = 2000
    config["make_dataset__list"] = []

    if args.query_type == "single_tree_percentage":
        try:
            # Configure the query
            query = queries_file.return_all_region_by_tree_type_percentage(
                tree_types[args.reference_tree],
                args.min_percentage,
                args.max_percentage,
            )

            ### TO DELETE --------------
            query = query.replace(";", "")
            query = query + " LIMIT 1000;"
            # --------------------------

            # Fetch data
            data = fetch_from_label_db(query)

            # Refromat data and split them by region
            label_data_creator(data, out_folder)

        except Exception as error:
            print("Invalid input parameters!", error)
            quit()

    elif args.query_type == "region_name":
        try:
            # Configure the query
            query = queries_file.return_all_labels_for_region(args.region)

            ### TO DELETE --------------
            query = query.replace(";", "")
            query = query + " LIMIT 1000;"
            # --------------------------

            # Fetch data
            data = fetch_from_label_db(query)

            # Reformat data
            features = []
            for index, row in data.iterrows():
                tmp = json.loads(row["label_area"])
                coordinates = find_bbox_bounds(tmp["coordinates"][0])
                features.append(
                    Feature(
                        geometry=Point(
                            (row["feature_coordinate_x"], row["feature_coordinate_y"]),
                            precision=14,
                        ),
                        properties={
                            "class": row["tree_type"],
                            "bbox_id": int(row["label_id"]),
                        },
                        bbox=[
                            coordinates[0],
                            coordinates[1],
                            coordinates[2],
                            coordinates[3],
                        ],
                    )
                )  # Be aware, the bbox id is not the same of the original label file

            # Save data
            create_label_file(features, out_folder, args.region)
            update_config(
                config, os.path.join(out_folder, args.region), row["raster_url"]
            )
            print("--created {} with {} points".format(args.region, len(features)))
            print("Requested data was created!")
        except Exception as error:
            print("Invalid input parameters!", error)
            quit()

    elif args.query_type == "temporal_interval":
        try:
            # Configure the query
            query = queries_file.return_all_region_for_temporal_interval(
                args.start_date, args.end_date
            )

            ### TO DELETE --------------
            query = query.replace(";", "")
            query = query + " LIMIT 1000;"
            # --------------------------

            # Fetch data
            data = fetch_from_label_db(query)

            # Refromat data and split them by region
            label_data_creator(data, out_folder)

        except Exception as error:
            print("Invalid input parameters!", error)
            quit()

    else:
        print("Invalid query type!")

    # Save configuration as YAML file
    with open(os.path.join(out_folder, "config.yaml"), "w") as outfile:
        yaml.dump(config, outfile, default_flow_style=False)
