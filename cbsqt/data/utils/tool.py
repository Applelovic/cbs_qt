from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class QueryTool(Query):

    def __init__(self, entities, engine):
        Query.__init__(self, entities=entities, session=sessionmaker(bind=engine)())

