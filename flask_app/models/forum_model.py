from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model
import re
ALPHANUMERIC = re.compile(r"^[a-zA-Z0-9]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DATABASE = 'travel'


class Forum:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.posted_by = data['posted_by']
        self.location = data['location']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# this is to save the user information to database
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO forum (name, posted_by, location, description, user_id) VALUES (%(name)s, %(posted_by)s, %(location)s, %(description)s, %(user_id)s);
        """

        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = """UPDATE forum SET name=%(name)s, location=%(location)s, description=%(description)s, updated_at=NOW() 
        WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    # pass in data to specify what you are deleting
    def delete(cls, data):
        query  = """
        DELETE FROM forum WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM forum JOIN users ON forum.user_id = users.id;
        """

        results = connectToMySQL(DATABASE).query_db(query)
        all_posts = []
        if results:
            for row in results:
                # create forum instance, if you don't pass row in the parenthesis, you will have duplicated row information, or the same forum
                this_post = cls(row)
                # isolate out the user data
                user_data = {
                    # copy everything from the row
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                # create user instance
                this_user = user_model.User(user_data)
                # store that user instance into a new attribute, inside of the forum instance
                this_post.owner = this_user
                # add to list of posts
                all_posts.append(this_post)
        return all_posts

    # pulls one
    @classmethod
    def get_one(cls,data):
        query = """
            SELECT * FROM forum WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    # get by id
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM forum JOIN users ON forum.user_id = users.id
        WHERE forum.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            # just getting one
            this_post = cls(results[0])
            row = results[0]
              # isolate out the user data
            user_data = {
                # copy everything from the row
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            this_user = user_model.User(user_data)
            this_post.owner = this_user
            return this_post
        return False

# ======================VALIDATOR==========================
    
    # validator for posts
    @staticmethod
    def validator(data):
        is_valid = True
        if len(data['name']) < 1:
            flash("*Name required")
            is_valid = False
        if len(data['description']) < 1:
            flash("*Description required")
            is_valid = False
        if len(data['location']) < 1:
            flash("*Location required")
            is_valid = False
        return is_valid
        
        


