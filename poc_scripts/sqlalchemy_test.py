# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 12:27:11 2015

@author: bethanygarcia
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine =  create_engine('postgres://bethanygarcia@localhost/USDA_Nutrition')
Base = declarative_base()
Base.metadata.reflect(engine)

from sqlalchemy.orm import relationship, backref

class Food_Desc(Base):
    __table__ = Base.metadata.tables['food_descriptions']
    

if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker, Query
    db_session = scoped_session(sessionmaker(bind=engine))
    for item in db_session.query(Food_Desc.ndb_no, Food_Desc.short_desc):
        print item