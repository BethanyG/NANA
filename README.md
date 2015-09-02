## NANA (Not Another Nutrition App)

Tracking nutritional intake is hard under the best circumstances, and is complicated by added restrictions (such as a diabetes or kidney disease).

**NANA** (**N**ot **A**nother **N**utrition **A**pp) enables users to get a quick nutritional analysis on a recipe as a starting point for more involved tracking of their intake.  Because the process starts with a URL (no typing in ingredients!), it lowers the activation energy for investigating and recording meal details.  It allows users to quickly flag ingredients/volumes that might be in their "red zone" -- or note items that will take more investigation.  This enables them to quickly start where they are adjusting serving size or changing key components (like salt).  Why do it all by hand if **NANA** can help?

### Implemented Features:

- Recipe cleaning an parsing from three supported websites
- Nutritional Analysis per ingredient via USDA Nutrient DB
- Clean, clear display of recipe and nutritional totals via customized nutrition label

### Future Features:
- Custom User Profiles for Nutrient Tracking
- Recipe Saving & Meal Planning
- Support for Additional Websites
- Ingredient Substitution and dynamic re-analysis

##Technologies
### Frontend / Framework
    Bootstrap
    CSS/HTML
    Nutritionix jQuery Label plug-in (www.nutritionix.com)
    JavaScript, jQuery, uderscore.js
    
    Flask, JinJa2, SQLAlchemy

#### Backend
	Python
	Beautiful Soup, nltk & associated packages, Pattern

	Postgresql, pg_trgm, fuzzystrmatch
	
## Structure
### server.py
    Core of the flask app routing.

### model.py
     Database representation for SQLAlchemy


### RecipeMaker.py
    Returns a current_recipe object

    Classes for creating Recipes and Ingredients:
        make_json
    	    Recipes have a method to JSONify themselves
    	    Ingredients have a method to JSONify themselves


    RecipeMaker Class, implemented as an absract base class:
	    parse_recipe classmethod
		      parses an incomming URL, and routs the resulting sitename to the correct 'maker'.  

	    process_url abstract method
		      sets a requirement that all child 'maker' classes implement this method for making a recipe object.

    Maker Child Classes - each 'maker' is a custom webscrapper targeted for a cooking website
      process_url
	    1) instantiates a Recipe object, 
	    2) parses the source HTML page into recipe parts using Beautiful Soup and nltk, 
	    3) instantiates and partially populates an array of Ingredient objects, 
	    4) returns to the parent class a Recipe object containing: 
	        * a list of Ingredient objects, one per ingredient for the recipe
	        * data attributes for title, source url, photo, description, preptime, 
	          cooktime, servings, and directions (where each is available)


###IngredientAnalyizer.py
    Returns Recipe objects, Ingredients, and Nutrition Summaries based on request.
    All methods are currently static.
  
  	set_ingredient_tokens
  		Preprocesses and tokenizes incoming recipie ingredients and converts unit of measure strings to numeric values
  	
  	query_for_ingredient
  		Queries DB for ingredient name matches
  	
  	query_for_ingredient_nutrition
  		1) queries DB for ingredient nutritional analaysis
  		2) summarizes individual ingredients into totals by recipe
  		3) sets a summary nutritional analysis in the Recpe object


###Postgresql DB with pg_trgm and fuzzystrmatch extenstions
  	* SQL-Created Tables and Postgresql COPY for data population
  	* CSV data files from USDA National Nutrient Database for Standard Reference R 27
  	* trgm index on Food_descriptions long_desc column to aid food term matching
  	* tsvector index based on long_desc column added to Food_descriptions 


##References & Aknowledgements

**USDA National Nutrient Database for Standard Reference, Release 27** 
U.S. Department of Agriculture, Agricultural Research Service. 2014.
[Nutrient Data Laboratory Home Page](http://www.ars.usda.gov/nutrientdata)

Nutritionx jQuery Label plug-in - with customizations(www.nutritionix.com)

######*Thank you Bob for all your object-oriented counseling (even if it was Java centric)!*
######*Thank you Katie for SQLAlchmey wrangling!  I will never see ORMs the same.*
######*Thank you Denise and Lavinia for through debugging, problemsolving and cheerleading*
######*Thank you StackOverflow.  None of this would work without the awsome help I've gotten through the site.*

EAFP! 
http://stackoverflow.com/questions/17015230/are-nested-try-except-blocks-in-python-a-good-programming-practice
https://docs.python.org/3/glossary.html#term-eafp


