from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id= data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

#CREATE
    @classmethod
    def create(cls, data): 
        query= '''
                INSERT INTO users
                (first_name,last_name,email,password)
                VALUES
                (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                '''
        return connectToMySQL(DB).query_db(query,data)

#Retrieve
    @classmethod
    def retrieve_one_user(cls, **data):
        query= 'SELECT * FROM users WHERE '
        where_str = ' AND '.join(f"{key}=%({key})s" for key in data)
        query += where_str + ';'
        results= connectToMySQL(DB).query_db(query,data)
        if results:
            return cls(results[0])

#VALIDATIONS
    @staticmethod
    def validate_reg(data):
        errors = {}

        if len(data['first_name']) < 2:
            errors['first_name'] = 'First name needs at least two characters fam...'
        if len(data['last_name']) < 2:
            errors['last_name'] = 'Last name needs at least two characters fam...'
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'That is not an email sir!'
        elif User.retrieve_one_user(email=data['email']):
            errors['email']= 'This email is already taken you THIEF!'
        if len(data['password']) < 8:
            errors['password']= 'Passwords obvi need at least 8 characters bro...'
        elif data['password'] != data['confirm_password']:
            errors['confirm_password']= 'Make em match homie!'

        for field,msg in errors.items():
            flash(msg,field)

        return len(errors)==0


    @staticmethod
    def validate_login(data):
        errors = {}
        user = User.retrieve_one_user(email=data['login_email'])

        if not user:
            errors['login'] = 'That would be incorrect...'
        elif not bcrypt.check_password_hash(user.password,data['login_password']):
            errors['login'] = 'That would be incorrect...'

        for field,msg in errors.items():
            flash(msg,field)

        return len(errors)==0