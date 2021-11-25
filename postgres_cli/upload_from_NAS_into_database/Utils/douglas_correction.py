import psycopg2
from shapely.geometry import box, Polygon
from psycopg2.extensions import register_adapter, AsIs
from shapely.geometry.base import BaseGeometry
import json
import sqlalchemy as db
import pprint


def get_label_feature_ids():
    engine = db.create_engine(
        "postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres"
    )
    connection = engine.connect()
    metadata = db.MetaData()
    label_feature = db.Table("label_feature", metadata, autoload=True, autoload_with=engine)
    query = db.select(label_feature).where(label_feature.columns.class_id == 0)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    print('LEN: ', len(ResultSet))
    douglas_fir_ids = [x[2] for x in ResultSet]
    return douglas_fir_ids


def update_label_feature(label_feature_id):
    """update class_id based on the label_feature_id"""
    sql = """ UPDATE label_feature
                SET class_id = %s
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
        cur.execute(sql, (0, label_feature_id))

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

    label_feature_ids = get_label_feature_ids()
    for label_feature_id in label_feature_ids:
        update_label_feature(label_feature_id)
