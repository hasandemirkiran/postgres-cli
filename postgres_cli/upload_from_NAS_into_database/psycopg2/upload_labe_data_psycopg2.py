import psycopg2
import psycopg2.extras as extras
from config import config
from extract_info import get_data_geoJson
import numpy
from psycopg2.extensions import register_adapter, AsIs
import sys


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)


def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn

    #     # close the communication with the PostgreSQL
    #     cur.close()
    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')


def fetch_data(table_name, conn):
    # create a cursor
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM public." + table_name + ";")

    # display the PostgreSQL database server version
    data = cursor.fetchall()
    print(data)

    cursor.close()


def upload_data(conn, table, file):
    # create a cursor
    cursor = conn.cursor()

    geoData_df = get_data_geoJson(file)
    small_df = geoData_df.head()

    # """
    # Using cursor.executemany() to insert the dataframe
    # """
    # # Create a list of tupples from the dataframe values
    # tuples = [tuple(x) for x in small_df.to_numpy()]
    # # Comma-separated dataframe columns
    # cols = [small_df['class_id'], small_df['feature_area'], small_df['label_id'] ]
    # # SQL quert to execute
    # # query  = "INSERT INTO %s(%s) VALUES %%s" % (table_name, cols)
    # print('==========')
    # print(small_df.loc[0])
    # print('==========')
    # cursor = conn.cursor()
    # try:
    #     # extras.execute_values(cursor, query, tuples)
    #     cursor.execute("INSERT INTO public.label_feature VALUES ('{}')".format(small_df.loc[0]))
    #     conn.commit()
    # except (Exception, psycopg2.DatabaseError) as error:
    #     print("Error: %s" % error)
    #     conn.rollback()
    #     cursor.close()
    #     return 1
    # print("execute_many() done")
    # cursor.close()

    if len(small_df) > 0:
        df_columns = list(small_df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)
        print("columns: ", columns)

        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

        # create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO public.{} ({}) {}".format(table, columns, values)

        cur = conn.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, small_df.values)
        conn.commit()
        cur.close()


if __name__ == "__main__":
    conn = connect()
    upload_data(conn, "label_feature_test", "./data/label_data/geoData.geojson")


# ---------------------
# Connect to PostgreSQL
# ---------------------
# t_host = "labeldb.cxitxpc33tur.eu-central-1.rds.amazonaws.com"
# t_port = "5432"
# t_dbname = "hasan_test"
# t_name_user = "ocell"
# t_password = "PdUfpcWSYh4y3Cg"
# data_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
# data_cursor = data_conn.cursor()

# file  = ''

# # ----------------------------------------
# # Function for retrieving form data (file)
# # ----------------------------------------
# def Upload_File():

#         # Reading a file
#         f = open(__file__, 'r')

#         #readline()
#         text = f.readlines(25)
#         print(text)
#         f.close()

#         blob_saved_file = request.files["file_name"]
#         # IMPORTANT: Be sure to have an item ID.
#         id_item = 52
#         # Call function for saving to Postgres, with two parameters
#         Save_File_To_Database(id_item, blob_saved_file)


# # ------------------------------------------
# # Function for saving the file to PostgreSQL
# # ------------------------------------------
# def Save_File_To_Database(id_item, blob_saved_file):
#     s = ""
#     s += "INSERT INTO tbl_saved_files"
#     s += "("
#     s += "id_item"
#     s += ", blob_saved_file"
#     s += ") VALUES ("
#     s += "(%id_item)"
#     s += ", '(%blob_saved_file)'"
#     s += ")"
#     # We recommend adding TRY here to trap errors.
#     data_cursor.execute(s, [id_item, blob_saved_file])
#     # Use commit here if you do not have auto-commits turned on.
