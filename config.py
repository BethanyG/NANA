# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 06:14:35 2015

@author: bethanygarcia

Thank you 
https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
for the config file I so convienently copied!
"""

import os

SQLALCHEMY_DATABASE_URI = 'postgresql://bethanygarca@localhost/USDA_Nutrition'




class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
