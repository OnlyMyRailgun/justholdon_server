from models import *
from flask.ext.restful import reqparse, Resource, fields, marshal_with, abort
from db import session
from weiboer import Weiboer
import os


def generate_random_password(length):
    return ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(length)))

wb = Weiboer()
parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('description', type=str)

user_fields = dict(
    username=fields.String,
    avatar_url=fields.String,
    description=fields.String,
    gender=fields.String,
    expired_in=fields.DateTime
)


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, uid):
        user = session.query(User).filter(User.uid == uid).one_or_none()
        if not user:
            abort(404, message="User {} doesn't exist".format(uid))
        return user

    @marshal_with(user_fields)
    def put(self, uid):
        user = session.query(User).filter(User.uid == uid).one_or_none()
        parsed_args = parser.parse_args()
        user.username = parsed_args['username']
        user.description = parsed_args['description']
        session.add(user)
        session.commit()
        return user, 200


class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        return session.query(User).all()

    def post(self):
        parsed_args = parser.parse_args()
        type = parsed_args['type']
        access_token = parsed_args['key']
        user = None
        if type == '1':
            wb_r = wb.get_detail_info(access_token)
            print wb_r
            user = User.query.filter_by(uid=wb_r[u'id']).first()
            already_regist = u'1'
            if user is None:
                already_regist = u'0'
                user = User(uid=wb_r[u'id'], username=wb_r[u'screen_name'], description=wb_r[u'description'],
                            avatar_url=wb_r[u'profile_image_url'], gender=wb_r[u'gender'],
                            password=generate_random_password(16))
                session.add(user)
                session.commit()

category_fields = dict(id=fields.Integer, name=fields.String)


class CategoryResource(Resource):
    @marshal_with(category_fields)
    def get(self):
        return session.query(Category).all()

habit_fields = dict(id=fields.Integer, name=fields.String, frequency=fields.Integer, tags=fields.String, description=fields.String)


class HabitResource(Resource):
    @marshal_with(habit_fields)
    def get(self, id):
        return session.query(Habit).filter(Habit.id == id).one_or_none()


class HabitListResource(Resource):
    @marshal_with(habit_fields)
    def get(self):
        return session.query(Habit).all()

    def post(self):
        pass

cultivation_fields = dict()


class CultivationResource(Resource):
    @marshal_with(cultivation_fields)
    def get(self):
        return session.query(Cultivation).filter(Cultivation)