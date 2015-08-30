# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 19:44:01 2015

@author: bethanygarcia

Everythng was broken until this post:
http://iswwwup.com/t/087c7349b801/python-typeerror-basequery-object-
is-not-callable-flask.html
"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import *
from RecipeMaker import *
#import RecipeMaker

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET', 'POST'])
def start_here():

    recipes = ['http://www.101cookbooks.com/archives/mung-yoga-bowl-recipe.html',
               'http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup',
               'http://www.manjulaskitchen.com/2015/07/14/paneer-bhurji',
               'http://www.manjulaskitchen.com/2015/08/14/eggless-omelet-vegan',
               'http://www.101cookbooks.com/archives/cocagne-bean-artichoke-salad-recipe.html',             
               'http://www.101cookbooks.com/archives/avocado-asparagus-tartine-recipe.html',
               'http://www.101cookbooks.com/archives/thai-zucchini-soup-recipe.html',
               'http://www.101cookbooks.com/archives/a-good-shredded-salad-recipe.html',
               'http://www.101cookbooks.com/archives/goldencrusted-brussels-sprouts-recipe.html',    
               'http://www.101cookbooks.com/archives/summer-berry-crisp-recipe.html',
               'http://www.101cookbooks.com/archives/caramelized-fennel-on-herbed-polenta-recipe.html']

    return render_template("homepage_template.html", recipes=recipes)


@app.route("/analysis-url", methods=['GET'])
#Bug:  When POST is used, RecipeMaker.parse_recipe is called twice in a row, and I can't
#figure out why!!!
def new_analysis_requested():
    
    recipe = request.args.get('recipe-urls')
    
    current_recipe = RecipeMaker.parse_recipe(recipe)
    recipe_details = Recipe.make_json(current_recipe)
    
    return render_template("analysis_url.html", recipe=recipe, recipe_details=recipe_details)


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
#alan@wakatime.com
def api_recipes_id(recipe_id):
    current_recipe = RecipeMaker.parse_recipe(url)
    recipe_details = Recipe.make_json(current_recipe)
  
    return recipe_details

@app.route("/test", methods=['GET'])
def test_query():
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
        			similarity(weights.measurement_desc, 'spear') > 0.035'''
           
    test = db.session.query(Food_Descriptions).from_statement(QUERY)

    display = {}
    for item in test:
        display[item.ndb_no] = item.long_desc
    
    return jsonify (display)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)
    
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
    
#'http://www.101cookbooks.com/archives/mung-yoga-bowl-recipe.html' - doesn't work
#'http://www.101cookbooks.com/archives/a-good-shredded-salad-recipe.html', - doesn't work    
#'http://www.101cookbooks.com/archives/goldencrusted-brussels-sprouts-recipe.html',    
#'http://www.101cookbooks.com/archives/summer-berry-crisp-recipe.html',
#'http://www.101cookbooks.com/archives/caramelized-fennel-on-herbed-polenta-recipe.html', - doesn't work


