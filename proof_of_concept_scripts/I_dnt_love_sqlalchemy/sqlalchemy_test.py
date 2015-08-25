# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 12:27:11 2015

@author: bethanygarcia
"""
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import text
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
#from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify

engine =  create_engine('postgres://bethanygarcia@localhost/USDA_Nutrition')
Base = declarative_base()
Base.metadata.reflect(engine)

from sqlalchemy.orm import relationship, backref

class Food_Desc(Base):
    __table__ = Base.metadata.tables['food_descriptions']


class Data_Derivation_Code(Base):
    __table__ = Base.metadata.tables['data_derivation_codes']


class Food_Descriptions(Base):
    __table__ = Base.metadata.tables['food_descriptions']

    ''' category_id = db.Column(db.String(5), db.ForeignKey('ndb_no'))
    category = db.relationship('ndb_no',
    backref=db.backref('ndb_no', lazy='dynamic'))'''


class Food_Group_Descriptions(Base):
    __table__ = Base.metadata.tables['food_group_descriptions']


#class Footnotes(Base):
#    __table__ = Base.metadata.tables['footnotes']


class Langual_Factor_Descriptions(Base):
    __table__ = Base.metadata.tables['langual_factor_descriptions']


class Langual_Factors(Base):
    __table__ = Base.metadata.tables['langual_factors']


class Nutrient_Data(Base):
    __table__ = Base.metadata.tables['nutrient_data']


class Nutrient_Definitions(Base):
    __table__ = Base.metadata.tables['nutrient_definitions']


class Source_Codes(Base):
    __table__ = Base.metadata.tables['source_codes']


class Sources_Of_Data(Base):
    __table__ = Base.metadata.tables['sources_of_data']


class Sources_Of_Data_Link(Base):
    __table__ = Base.metadata.tables['sources_of_data_link']


class User_Nutrients(Base):
    __table__ = Base.metadata.tables['user_nutrients']


class Weights(Base):
    __table__ = Base.metadata.tables['weights']


if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker, Query
    db_session = scoped_session(sessionmaker(bind=engine))
    
    
QUERY = '''
    SELECT
    		food_descriptions.ndb_no, food_descriptions.long_desc, 
            weights.amount, weights.measurement_desc, weights.gram_weight, 
            similarity(food_descriptions.long_desc, 'asparagus') AS sim_score, 
            similarity(weights.measurement_desc, 'spear') AS sim_score_measure
    FROM
    		food_descriptions
    JOIN
    		weights ON food_descriptions.ndb_no = weights.ndb_no
    WHERE
    		food_descriptions.long_desc % 'asparagus' 
    		AND 
    			similarity(food_descriptions.long_desc, 'asparagus') > 0.35
    		AND 
    			similarity(weights.measurement_desc, 'spear') > 0.035;
    '''
    
test = db_session.query(Food_Descriptions).from_statement(text(QUERY)).all()    
#new_test = dumps(test)

for Food_Descriptions in test:
    print Food_Descriptions.ndb_no, Food_Descriptions.long_desc
    print Food_Descriptions._sa_instance_state.__dict__
    
    
    
    #for item in db_session.query(Food_Desc.ndb_no, Food_Desc.short_desc):
        #print item