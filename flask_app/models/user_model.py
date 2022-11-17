from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
ALPHANUMERIC = re.compile(r"^[a-zA-Z0-9]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'travel'

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        user_instances = []
        if results:
            for row in results:
                this_user = cls(row)
                user_instances.append(this_user)
            return user_instances
        return []

    # check if something already exists
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users 
        WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
            #if it returns false, it will return user
        return cls(results[0])

# check if something already exists
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM users 
        WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        return cls(results[0])


# creating users
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)        
        """

        return connectToMySQL(DATABASE).query_db(query, data)

#===================VALIDATE USER============================

    @staticmethod
    def validator(data):
        is_valid = True
        print(data)
        if len(data['first_name']) < 2:
            flash("*First name must be atleast more than 2 characters.", 'reg')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("*Last name must be atleast more than 2 characters.", 'reg')
            is_valid = False
        elif not ALPHANUMERIC.match(data['first_name']):
            is_valid = False
            flash("No special characters in names please.")
        if len(data['email']) < 1:
            flash("*Email required", 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email", 'reg')
            is_valid = False
        else:
            user_data = {
                'email': data['email']
            }
            potential_user = User.get_by_email(user_data)
            # if we do get a user back, and they have the same email...
            if potential_user:
                flash("Email already taken", 'reg')
                # invalidate the submission
                is_valid = False
        if len(data['password']) < 8:
            flash("*Password required and must be atleast 8 characters long", 'reg')
            is_valid = False
        elif not data['password'] == data['confirm_pass']:
            flash("*Passwords do not match", 'reg')
            is_valid = False
        return is_valid

