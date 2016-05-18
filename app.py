# coding:UTF-8
import os
from flask.ext.restful import Api
from flask import Flask
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'default'])
api = Api(app)

from resources import UserResource, UserListResource, HabitListResource, HabitResource, CategoryResource
api.add_resource(UserListResource, '/users', endpoint='users')
api.add_resource(UserResource, '/users/<uid>', endpoint='user')
api.add_resource(HabitListResource, '/habits', endpoint='habits')
api.add_resource(HabitResource, '/habits/<id>', endpoint='habit')
api.add_resource(CategoryResource, '/categories', endpoint='categories')

if __name__ == '__main__':
    app.run()
