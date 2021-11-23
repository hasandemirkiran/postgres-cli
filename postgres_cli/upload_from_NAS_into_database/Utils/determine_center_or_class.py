import psycopg2

class_dict = {
    "Douglas": 0,
    "Fir": 1,
    "Larch": 2,
    "Spruce": 3,
    "Pine": 4,
    "Leaved Tree": 5,
    "Dead Tree": 6,
    "Young Tree": 7,
    "Background": 8,
    "Unknown": 9,
    "done": 10,
    "Dead Pine": 11,
    "Douglas fir": 12,
    "healthy": 13,
    "dead": 14,
    "affected": 15,
    "no class": 16,
}


def get_label_ids(label_session_id):
    """update raster_area based on the raster_url"""
    sql = "select id from label where session_id = %s"
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
        cur.execute(sql, (str(label_session_id),))

        # get the number of updated rows
        data = cur.fetchall()
        label_id_list = []
        for row in data:
            label_id_list.append(row[0])

        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return label_id_list


def get_label_feature_class_ids(label_id):
    """update raster_area based on the raster_url"""
    sql = "select class_id from label_feature where label_id = %s"
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
        cur.execute(sql, (str(label_id),))

        # get the number of updated rows
        data = cur.fetchall()
        class_id_list = []
        for row in data:
            class_id_list.append(row[0])

        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return class_id_list


if __name__ == "__main__":
    label_session_id = 51
    label_id_list = get_label_ids(label_session_id)

    for label_id in label_id_list:
        class_id_list = get_label_feature_class_ids(label_id)
        if class_id_list.count(9) != 0 and class_id_list.count(16) != 0:
            print(class_id_list.count(9))
            print(class_id_list.count(16))
        else:
            print("Could not find any unknown or no class in label id: ", label_id)
