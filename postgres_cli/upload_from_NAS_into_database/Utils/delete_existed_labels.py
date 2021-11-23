import pandas as pd
import sqlalchemy as db
import pprint

""" UNFINISHED """


def delete_bbox(df):
    engine = db.create_engine(
        "postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres_test"
    )
    connection = engine.connect()
    metadata = db.MetaData()
    label = db.Table("label", metadata, autoload=True, autoload_with=engine)
    query = db.select([label]).where()
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    for x in ResultSet:
        print(x)

    # for x in df['bbox']:
    #     if x in ResultSet:
    #         print('hello')

    # new_df =
    # return new_df


if __name__ == "__main__":
    print("Hello")
