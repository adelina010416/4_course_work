from flask import request
from flask_restx import Resource, Namespace

from implemented import user_service, users_schema, user_schema

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        res = users_schema.dump(all_users)
        return res, 200

    def post(self):
        req_json = request.json
        user_service.create(req_json)
        return "", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        res = user_schema.dump(user)
        return res, 200

    # def delete(self, uid):
    #     user_service.delete(uid)
    #     return "", 204
