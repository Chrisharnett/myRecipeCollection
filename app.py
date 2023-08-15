from flask import Flask, redirect, url_for, request, render_template, flash
import os
import pandas as pd
from werkzeug.utils import secure_filename
from forms import *
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nvmnkfwslzmnx.kj456/W?ERIU&WE(F*&/hksef;g98734:SP(&D'
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'img', '')

# Get the current list of recipe names
path = os.getcwd() + "/static/data"
recipeNames = []
for r in os.listdir(path):
    recipeNames.append(r.replace(".csv", ""))

@app.route('/', methods=['POST', 'GET'])
def myRecipeCollection():
    """
    Function to get random recipes to display on page
    :return:
    """
    random.shuffle(recipeNames)
    r1 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[0].lower().replace(" ", "_") + '.csv'), index_col=False)
    r2 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[1].lower().replace(" ", "_") + '.csv'), index_col=False)
    r3 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[2].lower().replace(" ", "_") + '.csv'), index_col=False)
    r4 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[3].lower().replace(" ", "_") + '.csv'), index_col=False)

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
            form.recipePicture.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic))
            df = pd.DataFrame(
                [{'name': recipeName, 'description': description, 'breakfast': breakfast, 'lunch': lunch,
                  'supper': supper, 'snack': snack, 'drink': drink, 'dessert': dessert,
                  'ingredients': ingredients, 'directions': directions, 'pic': pic}])
            df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipeName.lower().replace(" ", "_") + ".csv"))
            recipeNames.append(df['name'])
            flash('Recipe saved!')
            return redirect(url_for('addRecipe'))
        else:
            return render_template('addRecipe.html')

    return render_template('index.html', r1=r1.iloc[0], r2=r2.iloc[0], r3=r3.iloc[0], r4=r4.iloc[0])


@app.route('/addRecipe', methods=['POST', 'GET'])
def addRecipe():
    """
        Create and get data to make a recipe.
        :return: if form is complete, go to home page. Else reload addRecipe page
    """
    ## form functionality was moved to the index because of conflicts with the submit buttons.

    form = RecipeForm()
    return render_template('addRecipe.html', form=form)

@app.route('/recipeAdded.html')
def recipeAdded():
    form = RecipeForm()
    return render_template('recipeAdded.html', form=form)
@app.route('/viewRecipe/<recipeName>')
def viewRecipe(recipeName):
    """
    Function to parse the ingredients and description.
    :param recipeName:
    :return: recipe name, ingredients, description
    """
    mainRecipe = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                          recipeName.lower().replace(" ", "_") + '.csv'), index_col=False)
    ingredients = mainRecipe['ingredients'].str.split("\n")
    directions = mainRecipe['directions'].str.split("\n")

    recipeList = [recipe for recipe in recipeNames]
    recipeList.remove(mainRecipe.iloc[0]['name'].lower().replace(" ", "_"))
    random.shuffle(recipeList)
    r2 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeList[0].lower().replace(" ", "_") + '.csv'), index_col=False)
    r3 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeList[1].lower().replace(" ", "_") + '.csv'), index_col=False)
    r4 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeList[2].lower().replace(" ", "_") + '.csv'), index_col=False)

    return render_template('viewRecipe.html', mainRecipe=mainRecipe.iloc[0], ingredients=ingredients[0],
                           directions=directions[0],
                           r2=r2.iloc[0], r3=r3.iloc[0], r4=r4.iloc[0])


@app.route('/searchRecipes/<searchString>', methods=['POST', 'GET'])
def searchRecipes(searchString):
    searchResults = []
    if searchString == "":
        return browseRecipes()
    else:
        for name in recipeNames:
            df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                          name.lower().replace(" ", "_") + '.csv'), index_col=False)
            if df.iloc[0].str.contains(searchString).any():
                searchResults.append([df.iloc[0]['name'], df.iloc[0]['description'], df.iloc[0]['pic']])

    random.shuffle(recipeNames)

    r2 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[1].lower().replace(" ", "_") + '.csv'), index_col=False)
    r3 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[2].lower().replace(" ", "_") + '.csv'), index_col=False)
    r4 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[3].lower().replace(" ", "_") + '.csv'), index_col=False)
    return render_template('searchRecipes.html', r2=r2.iloc[0], r3=r3.iloc[0],
                           r4=r4.iloc[0], searchResults=searchResults)


@app.route('/browseRecipes', methods=['POST', 'GET'])
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
    if len(categories) > 0:
        for name in recipeNames:
            recipe = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                              name.lower().replace(" ", "_") + '.csv'), index_col=False)
            for category in categories:
                if recipe.iloc[0][category]:
                    recipesToBrowse.append(
                        [recipe.iloc[0]['name'], recipe.iloc[0]['description'], recipe.iloc[0]['pic']])

    else:
        for name in recipeNames:
            recipe = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                              name.lower().replace(" ", "_") + '.csv'), index_col=False)
            recipesToBrowse.append([recipe.iloc[0]['name'], recipe.iloc[0]['description'], recipe.iloc[0]['pic']])

    random.shuffle(recipeNames)

    r2 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[1].lower().replace(" ", "_") + '.csv'), index_col=False)
    r3 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[2].lower().replace(" ", "_") + '.csv'), index_col=False)
    r4 = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] +
                                  recipeNames[3].lower().replace(" ", "_") + '.csv'), index_col=False)

    return render_template('browseRecipes.html', r2=r2.iloc[0], r3=r3.iloc[0], r4=r4.iloc[0],
                           recipes=recipesToBrowse, form=categoryForm)


if __name__ == '__main__':
    app.run(debug=True, port=5003)
