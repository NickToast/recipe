from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

@app.route('/recipes/new')
def show_recipe_form():
    if 'user_id' not in session:
        return redirect ('/')

    return render_template('add_recipe.html')

@app.route('/edit/<int:recipe_id>')
def show_edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect ('/')
    one_recipe = Recipe.get_one({'recipe_id' : recipe_id})
    return render_template('edit_recipe.html', one_recipe=one_recipe)

@app.route('/recipes/edit/<int:recipe_id>', methods=['POST'])
def edit_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect('/edit/<int:recipe_id>')
    
    recipe_data = {
        **request.form,
        'recipe_id' : recipe_id
    }

    Recipe.update(recipe_data)

    return redirect('/recipes')

@app.route('/recipes/add', methods=['POST'])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    recipe_data = {
        **request.form, #takes everything in request.form and below to make the new data that we will use to make the recipe
        'user_id' : session['user_id']
    }
    Recipe.create_recipe(recipe_data)
    return redirect ('/recipes')


#SHOW ONE RECIPE
@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect ('/')
    one_user = User.get_user_by_id({'id' : session['user_id']})
    one_recipe = Recipe.get_one({'recipe_id' : recipe_id})

    return render_template('view_recipe.html', one_recipe=one_recipe, one_user=one_user)



#DELETE ONE RECIPE
@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect ('/')
    Recipe.delete(recipe_id)
    return redirect ('/recipes')