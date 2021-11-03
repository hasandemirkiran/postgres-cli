import sqlalchemy as db
import pprint 
import rasterio
from pyproj import Transformer 
import json

def get_ortho_urls_from_database():
    engine = db.create_engine('postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres')
    connection = engine.connect()
    metadata = db.MetaData()
    raster_info = db.Table('raster_info', metadata, autoload=True, autoload_with=engine)
    query = db.select(raster_info)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    ortho_url_list = []
    for x in ResultSet:
        ortho_url_list.append(x[5])
        
    return ortho_url_list

def get_bounds_of_orthos(ortho_url_list):
    
    ortho_url_bounds_dict = {}

    for ortho_url in ortho_url_list:
        raster = rasterio.open(ortho_url)
        raster_bounding_box = raster.bounds
        raster_format = raster.crs
        raster_bounds = []

        if raster_format != 'EPSG:4326':
            points_tuple = ((raster_bounding_box[0], raster_bounding_box[1]), (raster_bounding_box[2], raster_bounding_box[3]))
            transformer = Transformer.from_crs(3857, 4326)
            for pt in transformer.itransform(points_tuple):
                raster_bounds.append(pt[1])
                raster_bounds.append(pt[0])
        else:
            raster_bounds.append((raster_bounding_box[0], raster_bounding_box[1]))
            raster_bounds.append((raster_bounding_box[2], raster_bounding_box[3]))

        ortho_url_bounds_dict[ortho_url] = raster_bounds

    return ortho_url_bounds_dict 


if __name__ == "__main__":
    ortho_url_list = get_ortho_urls_from_database()
    ortho_url_bounds_dict = get_bounds_of_orthos(ortho_url_list)
    
    with open(r'Helper\ortho_url_bounds_dict.txt', 'w') as convert_file:
        convert_file.write(json.dumps(ortho_url_bounds_dict))