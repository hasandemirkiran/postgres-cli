import psycopg2
from shapely.geometry import box, Polygon
from psycopg2.extensions import register_adapter, AsIs
from shapely.geometry.base import BaseGeometry
import json
import sqlalchemy as db
import pprint


def get_ortho_ids_from_database():
    engine = db.create_engine(
        "postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres"
    )
    connection = engine.connect()
    metadata = db.MetaData()
    raster_info = db.Table("raster_info", metadata, autoload=True, autoload_with=engine)
    query = db.select(raster_info)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    ortho_id_url_tuple = []
    for x in ResultSet:
        ortho_id_url_tuple.append((x[0], x[5]))
    return ortho_id_url_tuple


def update_raster(raster_id, url):
    """update url based on the raster_id"""
    sql = """ UPDATE raster_info
                SET url = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com",
            database="postgres",
            user="postgres",
            password="PdUfpcWSYh4y3Cg",
        )
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        splitted_url = url.split("\\")
        new_url = ""
        for x in range(3, len(splitted_url)):
            new_url += "/" + splitted_url[x]

        cur.execute(sql, (new_url, raster_id))

        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


if __name__ == "__main__":

    ortho_id_url_tuple = get_ortho_ids_from_database()
    for tuple in ortho_id_url_tuple:
        update_raster(tuple[0], tuple[1])
