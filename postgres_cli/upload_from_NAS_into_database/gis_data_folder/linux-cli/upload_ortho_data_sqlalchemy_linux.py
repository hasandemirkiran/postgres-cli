from sqlalchemy import *
import url_finder_linux
import extract_info_linux
import pprint

# Creating SQLAlchemy's engine to use
engine = create_engine(
    "postgresql://ocell:PdUfpcWSYh4y3Cg@labeldb.cxitxpc33tur.eu-central-1.rds.amazonaws.com:5432/hasan_test"
)
path = "<PATH>"


ortho_last, label_last = url_finder_linux.last_sorted_dicts(path)

# Upload Ortho Files to Database
ortho_df = extract_info_linux.pick_from_ortho_dict(ortho_last)
ortho_df.rename(
    columns={"region_part": "name", "date": "recording_start_date"}, inplace=True
)
ortho_df_to_upload = ortho_df[
    ["id", "name", "gsd", "resolution", "recording_start_date", "url"]
]
pprint.pprint(ortho_df_to_upload)
ortho_df_to_upload.to_sql("raster_info", con=engine, if_exists="append", index=False)
