from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'recipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    #SAVE TO DATABASE
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    

    #UPDATE DATA
    @classmethod
    def update(cls, data):
        query = """
        UPDATE name
        SET variable_name = %(first_name)s,
        variable_name = %(name of form input)s,
        variable_name = %(name of form input)s,
        variable_name = %(name of form input)s,
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)


    #GET ONE BY ID METHOD
    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    

    #GET ONE BY EMAIL
    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


    #GET ALL 
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM users;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        name = []
        for row in results:
            name.append(cls(row))
        return name
    

    #VALIDATE USER
    @staticmethod
    def validate_user(data):
        is_valid = True
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(User.DB).query_db(query, data)
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters.', 'registration')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters.', 'registration')
            is_valid = False
        if len(results) >= 1:
            flash('Email is already taken.', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email.', 'registration')
            is_valid = False
        if len(data['password']) < 6:
            flash('Password must be 6 or more characters long!', 'registration')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash ('Passwords did not match.', 'registration')
            is_valid = False
        return is_valid


    #VALIDATE EMAIL
    @staticmethod
    def is_valid(email):
        is_valid = True
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;
            """
        results = connectToMySQL(User.DB).query_db(query, email)
        if not EMAIL_REGEX.match(email['email']):
            flash('Invalid email.', 'registration')
            is_valid = False
        return is_valid
    


