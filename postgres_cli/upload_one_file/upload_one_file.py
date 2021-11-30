import argparse
from postgres_cli.upload_one_file.upload_geoJson_file.upload_geoJson_file import (
    main_geoJson,
)
from postgres_cli.upload_one_file.upload_ortho_file.upload_ortho_file import main_ortho


def main_upload_file():
    parser = argparse.ArgumentParser(description="Process.")
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--geojson", action="store_true", help="To upload geojson file.")
    group.add_argument(
        "--ortho",
        action="store_true",
        help="To upload ortho file formatted as .gpkg or .tif.",
    )

    parser.add_argument("initial_path", type=str, help="Initial path of the NAS.")
    parser.add_argument("file", type=str, help="Path to the file")
    parser.add_argument(
        "-s",
        "--show_data",
        action="store_true",
        help="Optional comment to show the data or directly upload",
    )
    args = parser.parse_args()

    if args.geojson:
        main_geoJson(args)
    elif args.ortho:
        main_ortho(args)
    else:
        print("Please choose between one of geojson or ortho file to upload.")


if __name__ == "__main__":
    main_upload_file()
