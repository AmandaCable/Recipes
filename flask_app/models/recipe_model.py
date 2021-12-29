from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask_app import DB
from flask import flash


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cook_time = data['cook_time']
        self.recipe_date=data['recipe_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


#CREATE
    @classmethod
    def create(cls, data):        
        query ="INSERT INTO recipes (name, description, instructions, recipe_date, cook_time, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(recipe_date)s, %(cook_time)s, %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)

#RETRIEVE
    @classmethod
    def get_all_recipes(cls,data):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DB).query_db(query,data)
        
        all_recipes = []
        for row in results:
            recipe = cls(row)
            creator_data = {
                **row,
                'id': row['recipe.id'],
                'name': row['name'],
                'cook_time': row['cook_time']
            }
            all_recipes.append(recipe)
        return all_recipes

    @classmethod
    def get_one_recipe(cls,data):
        query ='''
                SELECT * FROM recipes 
                JOIN recipes
                ON user_id = users.id
                WHERE recipes.id=%(id)s;
                '''
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            row = results[0]
            recipe = cls(row)
            creator_data = {
                **row,
                'id': row['recipe.id'],
                'name': row['name'],
                'cook_time': row['cook_time']
            }
            recipe.created_by = user_model.User(creator_data)
            return recipe

#UPDATE
    @classmethod
    def update(cls,id,**data):
        query = "UPDATE recipes SET "
        set_str =', '.join(f"{key}=%({key})s" for key in data)
        query += set_str + " WHERE id=%(id)s;"
        
        return connectToMySQL(DB).query_db(query,{**data, 'id' :id})

#DELETE
    @classmethod
    def delete(cls,**data):
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
#VALIDATE
    @staticmethod
    def validate_recipe(data):
        errors = {}
        if len(data['name']) <2:
            errors['name']= "Recipe name must be at least 2 characters"
        if len(data['description']) <5:
            errors['description']= "Recipe description must be at least 5 characters"
        if len(data['instructions']) <5:
            errors['instructions']= "Recipe instructions must be at least 5 characters"
        if len(data['recipe_date']) <2:
            errors['recipe_date']= "Recipe date is required"
        
        for category,msg in errors.items():
            flash(msg,category)
        
        return len(errors)==0