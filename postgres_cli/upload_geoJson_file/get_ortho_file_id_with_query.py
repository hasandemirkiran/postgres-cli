import sqlalchemy as db
import pprint


def get_raster_id(raster_url):
    engine = db.create_engine(
        "postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres"
    )
    connection = engine.connect()
    metadata = db.MetaData()
    raster_info = db.Table("raster_info", metadata, autoload=True, autoload_with=engine)
    query = db.select([raster_info]).where(raster_info.columns.url == raster_url)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    raster_id = ResultSet[0][0]
    return raster_id


if __name__ == "__main__":
    # get_raster_id(
    #     "\\\\192.168.37.4\\gis_data\\customers\\Wallerstein\\Dist_12_13\\raster\\Orthos\\Ortho__Dist_12_13__67mm__1070mm__2021_06_14.gpkg"
    # )
    pass