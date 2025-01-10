""" from sqlalchemy import create_engine, select, MetaData, Table, Column, Integer,
String
from sqlalchemy.orm import sessionmaker
def function connectdb(dbname):
    engine = create_engine('sqlite:///%s' % dbname)
    metadata = MetaData(engine)
    caching=Table('caching',metadata,Column('id',Integer,PRIMARY_KEY=True AUTOINCREMENT),
    Column('query', String,UNIQUE),Column('result',String))
    Session=sessionmaker(bind=engine)
    session=Sessio()
    metadata.create_all(engine)


id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT UNIQUE,
            results TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP """