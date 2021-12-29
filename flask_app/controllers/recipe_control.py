

from flask import render_template,redirect,request,session
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User
from flask_app import app

#DISPLAY --> how many pages

@app.route('/recipes/<int:id>')
def view_recipe(id):
    context ={
        'logged_user':User.retrieve_one_user(id=session['id']),
        'recipes':Recipe.get_one_recipe(id=id)
    }
    return render_template('view_recipe.html', **context)

@app.route('/recipes/new')
def new_recipe():
    data = {
        User.retrieve_one_user(id=session['id'])
    }
    return render_template('new_recipe.html', data=data)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    context = {
        'logged_user': User.retrieve_one_user(id=session['id']),
        'recipes': Recipe.get_one_recipe(id=id)
    }
    return render_template('edit_recipe.html', **context)


#ACTIONS ---> how many action buttons there are

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    Recipe.create(**request.form, user_id=session['id'])
    return redirect('/dashboard')


@app.route('/recipes/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    Recipe.update(**request.form, id=id)
    return redirect(f'/recipes/{id}')


@app.route('/recipes/delete')
def delete_recipe(id):
    Recipe.delete(id=id)
    return redirect('/dashboard')