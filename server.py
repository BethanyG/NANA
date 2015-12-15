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
from IngredientAnalyzer import *

app = Flask(__name__)

# Required for Flask sessions & the debug toolbar
app.secret_key = "ABC"

# Raises an error if an undefined variable is used in Jinja2, instead of failing silently.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET', 'POST'])
def start_here():
    #retaining these for testing purposes.  Page has been modified to take typed-in URL
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
#FIX THIS:  When POST is used, RecipeMaker.parse_recipe is called twice in a row.

def new_analysis_requested():
    
    recipe_url = request.args.get('recipe-url')
    
    #Call RecipeMaker to use Beautiful Soup to scrape & clean recipe from Website    
    current_recipe = RecipeMaker.parse_recipe(recipe_url)
    
    #Call IngredientAnalyzer to identify & look up ingredients in USDADB    
    current_recipe = IngredientAnalyzer.analyze_recipe(current_recipe)
    
    #Call Recipe to Jsonify itself    
    recipe_details = Recipe.make_json(current_recipe)

    return render_template("analysis_url.html", recipe_url=recipe_url, recipe_details=recipe_details)


if __name__ == "__main__":
    # debug has to be True at the point that we invoke the DebugToolbarExtension
    #app.debug = True
    
    connect_to_db(app)
    
    # Use the DebugToolbar
    DebugToolbarExtension(app)    

    app.run(debug=True, host="0.0.0.0", port=5000)

