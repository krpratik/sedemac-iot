#SQLAlchemy ORM is used to perform SQL Transactions. It's an object mapper which maps tables in databases to classes in python
#SQL transactions sessions are created such data such that every file of the module can perform transactions by importing
# just this module


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

#Linking of database to SQLAlchemy engine. xyzdb is the name of database
engine = create_engine('postgresql:///xyzdb', convert_unicode=True)

#Metadata to restore earlier settings
metadata = MetaData(bind=engine)

#session created for SQL transactions
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
def init_db():
    metadata.create_all(bind=engine)
