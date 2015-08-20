# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 19:44:01 2015

@author: bethanygarcia
"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from RecipeMaker import *

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET', 'POST'])
def start_here():

    recipes = ['http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup/',
               'http://www.manjulaskitchen.com/2015/07/14/paneer-bhurji/',
               'http://www.manjulaskitchen.com/2015/08/14/eggless-omelet-vegan/',
               'http://www.101cookbooks.com/archives/cocagne-bean-artichoke-salad-recipe.html',
               'http://www.101cookbooks.com/archives/caramelized-fennel-on-herbed-polenta-recipe.html',
               'http://www.101cookbooks.com/archives/summer-berry-crisp-recipe.html',
               'http://www.101cookbooks.com/archives/avocado-asparagus-tartine-recipe.html',
               'http://www.101cookbooks.com/archives/goldencrusted-brussels-sprouts-recipe.html',
               'http://www.101cookbooks.com/archives/a-good-shredded-salad-recipe.html',
               'http://www.101cookbooks.com/archives/thai-zucchini-soup-recipe.html',
               'http://www.101cookbooks.com/archives/mung-yoga-bowl-recipe.html']

    return render_template("template_I_vi.html", recipes=recipes)


@app.route("/analysis-url", methods=['GET', 'POST'])
def new_analysis_requested():
    
    recipe = request.form.get('recipe-urls') 
    
    current_recipe = RecipeMaker.parse_recipe(recipe)
    recipe_details = RecipeMaker.make_recipe_json(current_recipe)
    
    return render_template("analysis_url.html", recipe=recipe, recipe_details=recipe_details)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()