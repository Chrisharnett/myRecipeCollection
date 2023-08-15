from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class RecipeForm(FlaskForm):
    recipeName = StringField('Recipe Name:', validators=[DataRequired()])
    recipeDescription = TextAreaField('Recipe Description:', validators=[DataRequired()])
    breakfastCategory = BooleanField('Breakfast')
    lunchCategory = BooleanField('Lunch')
    supperCategory = BooleanField('Supper')
    dessertCategory = BooleanField('Dessert')
    snackCategory = BooleanField('Snack')
    drinkCategory = BooleanField('Drink')
    recipeIngredients = TextAreaField('Ingredients:', validators=[DataRequired()])
    recipeDirections = TextAreaField('Directions:', validators=[DataRequired()])
    recipePicture = FileField('Picture:', validators=[FileRequired(), FileAllowed(['png', 'pdf', 'jpg', 'webp'],
                                                                                  'Invalid image format')])

class CategoryForm(FlaskForm):
    breakfastCategory = BooleanField('Breakfast')
    lunchCategory = BooleanField('Lunch')
    supperCategory = BooleanField('Supper')
    dessertCategory = BooleanField('Dessert')
    snackCategory = BooleanField('Snack')
    drinkCategory = BooleanField('Drink')

