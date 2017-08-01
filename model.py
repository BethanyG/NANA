# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 21:23:21 2015

@author: bethanygarcia
"""

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import text
from sqlalchemy.ext.serializer import loads, dumps

#Base = declarative_base()
#metadata = Base.metadata

db = SQLAlchemy()

class Data_Derivation_Code(db.Model):
    __tablename__ = 'data_derivation_codes'

    derivation_code = db.Column(db.String(4), primary_key=True)
    derivation_description = db.Column(db.String(120), nullable=False)


class Food_Descriptions(db.Model):
    __tablename__ = 'food_descriptions'

    ndb_no = db.Column(db.String(5), primary_key=True)
    fdgrp_cd = db.Column(db.String(4), nullable=False)
    long_desc = db.Column(db.String(200), nullable=False)
    short_desc = db.Column(db.String(60), nullable=False)
    comm_name = db.Column(db.String(100))
    manufact_name = db.Column(db.String(65))
    survey = db.Column(db.String(1))
    refuse_desc = db.Column(db.String(135))
    refuse = db.Column(db.Integer)
    sci_name = db.Column(db.String(65))
    n_factor = db.Column(db.Numeric)
    pro_factor = db.Column(db.Numeric)
    fat_factor = db.Column(db.Numeric)
    cho_factor = db.Column(db.Numeric)
    
    ''' category_id = db.Column(db.String(5), db.ForeignKey('ndb_no'))
    category = db.relationship('ndb_no',
    backref=db.backref('ndb_no', lazy='dynamic'))'''


class Food_Group_Descriptions(db.Model):
    __tablename__ = 'food_group_descriptions'

    fdgrp_cd = db.Column(db.String(4), primary_key=True)
    fdgrp_desc = db.Column(db.String(60), nullable=False)


class Footnotes(db.Model):
    __tablename__ = 'footnotes'

    ndb_no = db.Column(db.String(5), primary_key=True)
    footnote_no = db.Column(db.String(4), nullable=False)
    footnote_typed = db.Column(db.String(1), nullable=False)
    nutrient_no = db.Column(db.String(3))
    footnote_txt = db.Column(db.String(200), nullable=False)


class Langual_Factor_Descriptions(db.Model):
    __tablename__ = 'langual_factor_descriptions'

    factor_code = db.Column(db.String(5), primary_key=True)
    description = db.Column(db.String(140), nullable=False)


class Langual_Factors(db.Model):
    __tablename__ = 'langual_factors'

    langual_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ndb_no = db.Column(db.String(5))
    factor_code = db.Column(db.String(5))


class Nutrient_Data(db.Model):
    __tablename__ = 'nutrient_data'

    food_nutrient = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ndb_no = db.Column(db.String(5))
    nutrient_no = db.Column(db.String(3))
    nutrient_val = db.Column(db.Numeric, nullable=False)
    num_data_pts = db.Column(db.Numeric, nullable=False)
    std_error = db.Column(db.Numeric)
    source_code = db.Column(db.String(2), nullable=False)
    derivation_code = db.Column(db.String(4))
    ref_ndb_no = db.Column(db.String(5))
    add_nutr_mark = db.Column(db.String(1))
    num_studies = db.Column(db.Numeric)
    min_value = db.Column(db.Numeric)
    max_value = db.Column(db.Numeric)
    deg_of_freedom = db.Column(db.Numeric)
    lower_eb = db.Column(db.Numeric)
    upper_eb = db.Column(db.Numeric)
    stats_comment = db.Column(db.String(10))
    add_mod_date = db.Column(db.String(10))
    confid_code = db.Column(db.String(1))


class Nutrient_Definitions(db.Model):
    __tablename__ = 'nutrient_definitions'

    nutrient_no = db.Column(db.String(3), primary_key=True)
    units = db.Column(db.String(7), nullable=False)
    tag_name = db.Column(db.String(20))
    nutrient_desc = db.Column(db.String(60), nullable=False)
    num_decimals = db.Column(db.String(1), nullable=False)
    sr_order = db.Column(db.Numeric, nullable=False)


class Source_Codes(db.Model):
    __tablename__ = 'source_codes'

    source_code = db.Column(db.String(2), primary_key=True)
    source_code_desc = db.Column(db.String(60), nullable=False)


class Sources_Of_Data(db.Model):
    __tablename__ = 'sources_of_data'

    data_source_id = db.Column(db.String(6), primary_key=True)
    authors = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(4))
    journal = db.Column(db.String(135))
    volume_city = db.Column(db.String(16))
    issue_state = db.Column(db.String(5))
    start_page = db.Column(db.String(5))
    end_page = db.Column(db.String(5))


class Sources_Of_Data_Link(db.Model):
    __tablename__ = 'sources_of_data_link'

    link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ndb_no = db.Column(db.String(5))
    nutrient_no = db.Column(db.String(3))
    data_source_id = db.Column(db.String(6))


class User_Nutrients(db.Model):
    __tablename__ = 'user_nutrients'

    user_id = db.Column(db.Numeric, primary_key=True, nullable=False)
    nutrient_no = db.Column(db.String(3), primary_key=True, nullable=False)
    nutrient_desc = db.Column(db.String(60), nullable=False)


class Weights(db.Model):
    __tablename__ = 'weights'

    weight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ndb_no = db.Column(db.String(5))
    sequence_no = db.Column(db.String(2))
    amount = db.Column(db.Numeric, nullable=False)
    measurement_desc = db.Column(db.String(84), nullable=False)
    gram_weight = db.Column(db.Numeric, nullable=False)
    num_data_pts = db.Column(db.Numeric)
    std_deviation = db.Column(db.Numeric)


def connect_to_db(app):
    """Connect the dat(db.Model to our Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bethanygarcia@localhost/USDA_Nutrition'
    #bind here for second user db uri
    db.app = app
    db.init_app(app)

   
if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the dat(db.Model directly.

    from server import app
    connect_to_db(app)
    print ("Connected to DB.")
    

#for item in Food_Descriptions.query(Food_Descriptions.ndb_no, Food_Descriptions.short_desc):
#        print item