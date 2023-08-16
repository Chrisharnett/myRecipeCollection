from flask import Flask, redirect, url_for, request, render_template, flash
import os
import pandas as pd
from werkzeug.utils import secure_filename
from forms import *
import random

# LATEST Now

application = Flask(__name__)

application.config['SECRET_KEY'] = 'nvmnkfwslzmnx.kj456/W?ERIU&WE(F*&/hksef;g98734:SP(&D'
application.config['SUBMITTED_DATA'] = os.path.join('static', 'data', '')
application.config['SUBMITTED_IMG'] = os.path.join('static', 'img', '')

# Get the current list of recipe names
path = os.getcwd() + "/static/data"
def recipeNames():
    recipeNames = []
    for r in os.listdir(path):
        recipeNames.append(r.replace(".csv", ""))
    return recipeNames

@application.route('/', methods=['POST', 'GET'])
def myRecipeCollection():
    """
    Function to get random recipes to display on page
    :return:
    """
    allRecipes = recipeNames()
    random.shuffle(allRecipes)
    r1 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[0].lower().replace(" ", "_") + '.csv'), index_col=False)
    r2 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[1].lower().replace(" ", "_") + '.csv'), index_col=False)
    r3 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[2].lower().replace(" ", "_") + '.csv'), index_col=False)
    r4 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[3].lower().replace(" ", "_") + '.csv'), index_col=False)

    if request.method == 'POST' and request.form['action'] == 'search':
        searchString = request.form['searchString']
        return redirect(url_for('searchRecipes', searchString=searchString))
    elif request.method == 'POST' and request.form['action'] == 'newRecipe':
        form = RecipeForm()
        if form.validate_on_submit():
            recipeName = form.recipeName.data
            description = form.recipeDescription.data
            breakfast = form.breakfastCategory.data
            lunch = form.lunchCategory.data
            supper = form.supperCategory.data
            snack = form.snackCategory.data
            drink = form.drinkCategory.data
            dessert = form.dessertCategory.data
            ingredients = form.recipeIngredients.data
            directions = form.recipeDirections.data
            pic = recipeName.lower().replace(" ", "_") + "." + \
                  secure_filename(form.recipePicture.data.filename).split('.')[-1]
            form.recipePicture.data.save(os.path.join(application.config['SUBMITTED_IMG'] + pic))
            df = pd.DataFrame(
                [{'name': recipeName, 'description': description, 'breakfast': breakfast, 'lunch': lunch,
                  'supper': supper, 'snack': snack, 'drink': drink, 'dessert': dessert,
                  'ingredients': ingredients, 'directions': directions, 'pic': pic}])
            df.to_csv(os.path.join(application.config['SUBMITTED_DATA'] + recipeName.lower().replace(" ", "_") + ".csv"))
            # recipeNames.append(df.iloc[0]['name'])
            flash('Recipe saved!')
            return redirect(url_for('addRecipe'))
        else:
            return render_template('addRecipe.html')

    return render_template('index.html', r1=r1.iloc[0], r2=r2.iloc[0], r3=r3.iloc[0], r4=r4.iloc[0])


@application.route('/addRecipe', methods=['POST', 'GET'])
def addRecipe():
    """
        Create and get data to make a recipe.
        :return: if form is complete, go to home page. Else reload addRecipe page
    """
    ## form functionality was moved to the index because of conflicts with the submit buttons.

    form = RecipeForm()
    return render_template('addRecipe.html', form=form)

@application.route('/recipeAdded.html')
def recipeAdded():
    form = RecipeForm()
    return render_template('recipeAdded.html', form=form)
@application.route('/viewRecipe/<recipeName>')
def viewRecipe(recipeName):
    """
    Function to parse the ingredients and description.
    :param recipeName:
    :return: recipe name, ingredients, description
    """
    mainRecipe = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                          recipeName.lower().replace(" ", "_") + '.csv'), index_col=False)
    ingredients = mainRecipe['ingredients'].str.split("\n")
    directions = mainRecipe['directions'].str.split("\n")

    allRecipes = recipeNames()
    recipeList = [recipe for recipe in allRecipes]
    recipeList.remove(mainRecipe.iloc[0]['name'].lower().replace(" ", "_"))
    random.shuffle(recipeList)
    r2 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  recipeList[0].lower().replace(" ", "_") + '.csv'), index_col=False)
    r3 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  recipeList[1].lower().replace(" ", "_") + '.csv'), index_col=False)
    r4 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  recipeList[2].lower().replace(" ", "_") + '.csv'), index_col=False)

    return render_template('viewRecipe.html', mainRecipe=mainRecipe.iloc[0], ingredients=ingredients[0],
                           directions=directions[0],
                           r2=r2.iloc[0], r3=r3.iloc[0], r4=r4.iloc[0])


@application.route('/searchRecipes/<searchString>', methods=['POST', 'GET'])
def searchRecipes(searchString):
    allRecipes = recipeNames()
    searchResults = []
    if searchString == "":
        return browseRecipes()
    else:
        for name in allRecipes:
            df = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                          name.lower().replace(" ", "_") + '.csv'), index_col=False)
            if df.iloc[0].str.contains(searchString).any():
                searchResults.append([df.iloc[0]['name'], df.iloc[0]['description'], df.iloc[0]['pic']])

    random.shuffle(allRecipes)

    r2 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[1].lower().replace(" ", "_") + '.csv'), index_col=False)
    r3 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[2].lower().replace(" ", "_") + '.csv'), index_col=False)
    r4 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[3].lower().replace(" ", "_") + '.csv'), index_col=False)
    return render_template('searchRecipes.html', r2=r2.iloc[0], r3=r3.iloc[0],
                           r4=r4.iloc[0], searchResults=searchResults)


@application.route('/browseRecipes', methods=['POST', 'GET'])
def browseRecipes():
    """
        Function to get random recipes to display on page
        :return:
        """
    categories = []
    categoryForm = CategoryForm()
    if categoryForm.validate_on_submit():
        breakfast = categoryForm.breakfastCategory.data
        if breakfast:
            categories.append('breakfast')
        lunch = categoryForm.lunchCategory.data
        if lunch:
            categories.append('lunch')
        supper = categoryForm.supperCategory.data
        if supper:
            categories.append('supper')
        snack = categoryForm.snackCategory.data
        if snack:
            categories.append('snack')
        drink = categoryForm.drinkCategory.data
        if drink:
            categories.append('drink')
        dessert = categoryForm.dessertCategory.data
        if dessert:
            categories.append('dessert')

    recipesToBrowse = []
    allRecipes = recipeNames()
    if len(categories) > 0:
        for name in allRecipes:
            recipe = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                              name.lower().replace(" ", "_") + '.csv'), index_col=False)
            for category in categories:
                if recipe.iloc[0][category]:
                    rName = recipe.iloc[0]['name']
                    if len(recipesToBrowse) == 0:
                        recipesToBrowse.append(
                            [recipe.iloc[0]['name'], recipe.iloc[0]['description'], recipe.iloc[0]['pic']])
                    else:
                        if any(rName in recipe for recipe in recipesToBrowse):
                            continue
                        else:
                            recipesToBrowse.append(
                                [recipe.iloc[0]['name'], recipe.iloc[0]['description'], recipe.iloc[0]['pic']])

    else:
        for name in allRecipes:
            recipe = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                              name.lower().replace(" ", "_") + '.csv'), index_col=False)
            recipesToBrowse.append([recipe.iloc[0]['name'], recipe.iloc[0]['description'], recipe.iloc[0]['pic']])

    random.shuffle(allRecipes)

    r2 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[1].lower().replace(" ", "_") + '.csv'), index_col=False)
    r3 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[2].lower().replace(" ", "_") + '.csv'), index_col=False)
    r4 = pd.read_csv(os.path.join(application.config['SUBMITTED_DATA'] +
                                  allRecipes[3].lower().replace(" ", "_") + '.csv'), index_col=False)

    return render_template('browseRecipes.html', r2=r2.iloc[0], r3=r3.iloc[0], r4=r4.iloc[0],
                           recipes=recipesToBrowse, form=categoryForm)


if __name__ == '__main__':
    application.run(debug=True, port=5001)
