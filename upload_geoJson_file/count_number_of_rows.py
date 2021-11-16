import psycopg2

def count_rows_of_table(table_name):
    """ update raster_area based on the raster_url """
    sql = "select count(*) from " + table_name
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com",
            database="postgres",
            user="postgres",
            password="PdUfpcWSYh4y3Cg"

        )
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql)

        # get the number of updated rows
        data = cur.fetchall()
        # print('Number of rows in ', table_name, ' table', data[0][0])
        return (data[0][0])

        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    count_rows_of_table('label_feature')
