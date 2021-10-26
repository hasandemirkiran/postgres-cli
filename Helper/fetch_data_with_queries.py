import sqlalchemy as db
import pprint

engine = db.create_engine('postgresql://ocell:PdUfpcWSYh4y3Cg@labeldb.cxitxpc33tur.eu-central-1.rds.amazonaws.com:5432/hasan_test')
connection = engine.connect()
metadata = db.MetaData()
raster_info = db.Table('raster_info', metadata, autoload=True, autoload_with=engine)
query = db.select([raster_info]).where(raster_info.columns.name == 'Dist_12_13')
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
pprint.pprint(ResultSet)