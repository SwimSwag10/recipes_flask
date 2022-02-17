from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
  def __init__(self,data):
    self.id = data['id']
    self.name = data['name']
    self.description = data['description']
    self.instructions = data['instructions']
    self.under30 = data['under30']
    self.date_made = data['date_made']
    self.user_id = data['user_id']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  # CREATE

  @classmethod
  def create_recipe(cls,data):
    query = """
    INSERT INTO recipes (name, description, instructions, under30, date_made, user_id) 
    VALUES (%(name)s,%(description)s,%(instructions)s,%(under30)s,%(date_made)s,%(user_id)s)
    ;"""
    return connectToMySQL('recipes_schema').query_db(query,data)

  # READ

  @classmethod
  def get_all(cls):
    query = """SELECT * FROM recipes;"""
    result = connectToMySQL('recipes_schema').query_db(query)
    recipes = []
    for row in result:
      recipes.append(cls(row))
    return result

  @classmethod
  def get_one_recipe(cls, data):
    query = "SELECT * FROM recipes WHERE id = %(id)s;"
    results = connectToMySQL('recipes_schema').query_db(query, data)
    return cls(results[0])

  # UPDATE

  @classmethod
  def update(cls, data):
    query = """UPDATE recipes 
    SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under30=%(under30)s, date_made=%(date_made)s,updated_at=NOW() 
    WHERE id = %(id)s
    ;"""
    return connectToMySQL('recipes_schema').query_db(query,data)

  # DELETE

  @classmethod
  def delete(cls, data):
    query = "DELETE FROM recipes WHERE id = %(id)s"
    return connectToMySQL('recipes_schema').query_db(query,data)
  
  @staticmethod
  def validate_recipe( recipe ):
    is_valid = True
    # -------------------------------- validating first_name --------------------------------
    if len(recipe['name']) < 3:
      flash("Name must be longer than 2 characters", 'recipe')
      is_valid = False
    # -------------------------------- validating last_name --------------------------------
    if len(recipe['description']) < 3:
      flash("Description must be longer than 2 characters", 'recipe')
      is_valid = False
    # -------------------------------- validating password --------------------------------
    if len(recipe['instructions']) < 3:
      flash("Instructions must be longer than 2 characters", 'recipe')
      is_valid = False

    # if recipe['date_made'] == "":
    #   flash("Please enter a date","recipe")
    #   is_valid = False

    return is_valid