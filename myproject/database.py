#SQLAlchemy ORM is used to perform SQL Transactions .
#

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql:///xyzdb', convert_unicode=True)
metadata = MetaData(bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
def init_db():
    metadata.create_all(bind=engine)
