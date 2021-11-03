import sqlalchemy as db
import pprint

engine = db.create_engine('postgresql://postgres:PdUfpcWSYh4y3Cg@geodb.c6pejgcymcj0.eu-central-1.rds.amazonaws.com:5432/postgres')
connection = engine.connect()
metadata = db.MetaData()
raster_info = db.Table('raster_info', metadata, autoload=True, autoload_with=engine)
query = db.select([raster_info]).where(raster_info.columns.name == 'Eleonorenwald_Merged')
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
pprint.pprint(ResultSet)