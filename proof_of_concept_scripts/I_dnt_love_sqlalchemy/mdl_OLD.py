# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 19:32:08 2015

@author: bethanygarcia
"""
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, create_engine
from special_bind_code import MySQLAlchemy

db = MySQLAlchemy()
metadata=MetaData()
engine = create_engine('postgres://bethanygarcia@localhost/USDA_Nutrition')


class Food_Descriptions(db.Model):
    __tablename__ = 'food_descriptions' 
    #db.metadata.tables('food_descriptions')
    #food_desc = Table('food_descriptions', metadata, autoload=True, autoload_with=engine)    

#__table__ = db.metadata.tables['food_descriptions']
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use postgres database
    # app.config.['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bethanygarcia@localhost/USDA_Nutrition'
    app.config['SQLALCHEMY_BINDS'] = {'USDA_Nutrition':'postgres://usr/local/var/postgres'}    
    #db.app = app
    db.init_app(app)
    #db.metadata.reflect(engine)    
    #with app.app_context():    
    #    metadata.bind = app
    
    #db.metadata.reflect(app=app) 
    #db.Model.metadata.reflect(app)
if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    
#for item in Food_Descriptions.query(Food_Descriptions.ndb_no, Food_Descriptions.short_desc):
#        print item