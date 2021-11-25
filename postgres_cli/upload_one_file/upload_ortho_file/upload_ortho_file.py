from sqlalchemy import *
import argparse
import uuid
import pandas as pd
import pprint


def pick_from_ortho_dict(url):
    ortho_list_to_upload = []

    x = url.split("/")
    y = x[-1].split("__")
    region_part = y[1]
    if len(y) == 5 and y[-1] != "CIR.gpkg":
        gsd = y[2]
        resolution = y[3]
        date = y[4].split(".")[0]
    else:
        if int(y[2][:-2]) < 100:
            gsd = y[2]
            resolution = -1
        else:
            gsd = -1
            resolution = y[2]

        date = y[3].split(".")[0]
    extn = x[-1].split(".")[-1]

    info = {
        "customer": x[-5],
        "region": x[-4],
        "region_part": region_part,
        "gsd": gsd,
        "resolution": resolution,
        "date": date,
        "url": url,
        "extn": extn,
    }
    ortho_list_to_upload.append(info)

    id = [uuid.uuid4().int & (1 << 31) - 1 for x in range(len(ortho_list_to_upload))]
    ortho_df = pd.DataFrame(ortho_list_to_upload)
    ortho_df.insert(0, "id", id)

    return ortho_df


def main_ortho(args):

    engine = create_engine(
        "postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres"
    )
    url = args.initial_path + args.file

    ortho_df = pick_from_ortho_dict(url)

    if args.show_data:
        pprint.pprint(ortho_df)
    else:
        ortho_df.rename(
            columns={"region_part": "name", "date": "recording_start_date"},
            inplace=True,
        )
        ortho_df_to_upload = ortho_df[
            ["id", "name", "gsd", "resolution", "recording_start_date", "url"]
        ]
        ortho_df_to_upload.to_sql(
            "raster_info", con=engine, if_exists="append", index=False
        )


if __name__ == "__main__":
    main_ortho()
