import psycopg2
from shapely.geometry import box, Polygon
from psycopg2.extensions import register_adapter, AsIs
from shapely.geometry.base import BaseGeometry
import sqlalchemy as db
import pprint


def fetch_data():
    sql = """ SELECT label_session.id, label_session.raster_info_id, raster_info.url
                FROM label_session
                INNER JOIN raster_info ON label_session.raster_info_id=raster_info.id;"""
    conn = None
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
        cur.execute(sql)

        # get the number of updated rows
        label_session_id_raster_id_url = cur.fetchall()

        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return label_session_id_raster_id_url


def update_label_session(user_id, label_session_id):
    """update creator_user_id based on the label_session_id"""
    sql = """ UPDATE label_session
                SET creator_user_id = %s
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

        cur.execute(sql, (user_id, label_session_id))

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
    label_session_id_raster_id_url = fetch_data()
    for label_session_entry in label_session_id_raster_id_url:
        update_label_session(label_session_entry[0], label_session_entry[2])