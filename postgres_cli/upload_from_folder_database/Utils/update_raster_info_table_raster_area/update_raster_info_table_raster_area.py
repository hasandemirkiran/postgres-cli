import psycopg2
from shapely.geometry import box, Polygon 
from psycopg2.extensions import register_adapter, AsIs
from shapely.geometry.base import BaseGeometry
import json 

def geometry_adaptor(geom: BaseGeometry):
    return AsIs(f"ST_WKTToSQL('{geom.wkt}')")

    
# def adapt_Polygon(polygon: Polygon):
#     return AsIs(f"ST_WKTToSQL('{polygon}')")

register_adapter(BaseGeometry, geometry_adaptor)

def update_raster(raster_url, raster_area):
    """ update raster_area based on the raster_url """
    sql = """ UPDATE raster_info
                SET raster_area = %s
                WHERE url = %s"""
    conn = None
    updated_rows = 0
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
        cur.execute(sql, (raster_area, raster_url))

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

    with open(r"Utils\ortho_url_bounds_dict.txt") as f:
        data = f.read()
    ortho_url_bounds_dict = json.loads(data)
    
    for url in ortho_url_bounds_dict:
        update_raster(url, box(ortho_url_bounds_dict[url][0],ortho_url_bounds_dict[url][1],ortho_url_bounds_dict[url][2],ortho_url_bounds_dict[url][3]))
