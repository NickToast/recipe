from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Recipe:
    DB = 'recipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        # self.recipe_owner = {}


    #SAVE TO DATABASE
    @classmethod
    def create_recipe(cls, data):
        query = """
        INSERT INTO recipes (name, description, instructions, under_30, date_made, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(user_id)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    #UPDATE DATA
    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipes
        SET name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s,
        under_30 = %(under_30)s,
        date_made = %(date_made)s
        WHERE recipes.id = %(recipe_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    

    #VALIDATE INPUT DATA FOR RECIPE
    @staticmethod
    def validate_recipe(new_recipe):
        is_valid = True
        if len(new_recipe['name']) < 3:
            flash('Name must be at least 3 characters.', 'recipe')
            is_valid = False
        if len(new_recipe['description']) < 3:
            flash('Description must be at least 3 characters.', 'recipe')
            is_valid = False
        if len(new_recipe['instructions']) < 3:
            flash('Instructions must be at least 3 characters.', 'recipe')
            is_valid = False
        if len(new_recipe['date_made']) < 1:
            flash('Date created or made is required.', 'recipe')
            is_valid = False
        if 'under_30' not in new_recipe:
            flash('Under 30 minutes question is required.', 'recipe')
            is_valid = False
        return is_valid
    

    #GET ALL RECIPES
    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        JOIN users ON users.id = recipes.user_id
        """
        result = connectToMySQL(cls.DB).query_db(query)
        all_recipes = []

        for row in result:
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'password' : row['password'],
                'email' : row['email'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            one_recipe = cls(row)
            one_recipe.recipe_owner = user_model.User(user_data)
            all_recipes.append(one_recipe)

        return all_recipes
    

    #CLASS GET ONE METHOD BY ID 
    @classmethod
    def get_one(cls, data):
        query = """
        SELECT * FROM recipes
        JOIN users ON users.id = recipes.user_id
        WHERE recipes.id = %(recipe_id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        one_recipe = cls(result[0])

        user_data = {
                'id' : result[0]['users.id'],
                'first_name' : result[0]['first_name'],
                'last_name' : result[0]['last_name'],
                'password' : result[0]['password'],
                'email' : result[0]['email'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at']
            }
        
        one_recipe.recipe_owner = user_model.User(user_data)

        return one_recipe
    

    #DELETE METHOD
    @classmethod
    def delete(cls, recipe_id):
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s;
        """
        data = {'id' : recipe_id}
        return connectToMySQL(cls.DB).query_db(query, data)