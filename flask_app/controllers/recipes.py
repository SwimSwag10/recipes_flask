from flask import render_template,request, redirect, flash, session
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
  if 'user_id' not in session:
    return redirect('/logout')
  if not Recipe.validate_recipe(request.form):
    return redirect('/recipe/dashboard')
  data = {
    "name": request.form["name"],
    "description": request.form["description"],
    "instructions": request.form["instructions"],
    "under30": int(request.form["under30"]),
    "date_made": request.form["date_made"],
    "user_id": session["user_id"]
  }
  Recipe.create_recipe(data)
  return redirect('/dashboard')


# READ

@app.route('/recipe/dashboard')
def recipes_dashboard():
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    'id' : session['user_id']
  }
  return render_template('recipes_new.html', user=User.get_by_id(data))

@app.route('/recipe/<int:id>')
def show_recipe(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id":id
  }
  user_data = {
    "id":session['user_id']
  }
  return render_template("recipes.html", recipe=Recipe.get_one_recipe(data), user=User.get_by_id(user_data))

# UPDATE

@app.route('/recipe/update/<int:id>', methods=['POST'])
def update_recipe(id):
  print('??????????????????????????')
  if 'user_id' not in session:
      return redirect('/logout')
  if not Recipe.validate_recipe(request.form):
    return redirect('/dashboard')
  print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
  data = {
    "name": request.form["name"],
    "description": request.form["description"],
    "instructions": request.form["instructions"],
    "under30": int(request.form["under30"]),
    "date_made": request.form["date_made"],
    "id" : id
  }
  Recipe.update(data)
  return redirect('/dashboard')

@app.route('/recipe/update/form/<int:id>')
def recipe_update_form(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id":id
  }
  user_data = {
    "id":session['user_id']
  }
  return render_template("recipes_edit.html", recipe=Recipe.get_one_recipe(data), user=User.get_by_id(user_data))

# DELETE

@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id" : id
  }
  Recipe.delete(data)
  return redirect('/dashboard')