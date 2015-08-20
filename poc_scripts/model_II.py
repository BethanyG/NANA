# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 21:23:21 2015

@author: bethanygarcia
"""

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, create_engine
#from special_bind_code import MySQLAlchemy

db = SQLAlchemy()
db.reflect(bind='__all__', app=None)

class Food_Descriptions(db.Model):
    __table__ = db.Model.metadata.tables['Food_Descriptions']
    
    
def connect_to_db(app):
    """Connect the database to our Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bethanygarcia@localhost/USDA_Nutrition'
    #db.init_app(app)
    db.app = app
    db.Model.get_binds(app=None)
    db.Model.get_tables_for_bind(bind=None)
    

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    
#for item in Food_Descriptions.query(Food_Descriptions.ndb_no, Food_Descriptions.short_desc):
#        print item