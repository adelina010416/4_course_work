from flask import request
from flask_restx import Resource, Namespace

from implemented import user_service, users_schema, user_schema
from decorators import auth_required

user_ns = Namespace('user')


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        """Реализует переход на личную страницу по токену"""
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        user = user_service.get_one_owner(token)
        res = user_schema.dump(user)
        return res, 200

    def patch(self):
        token = request.headers['Authorization'].split('Bearer ')[-1]
        data = request.json
        user_service.partially_update(token, data)
        return "", 201


@user_ns.route('/users')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        res = users_schema.dump(all_users)
        return res, 200


@user_ns.route('/<int:uid>')
class UserGuestView(Resource):
    @auth_required
    def get(self, uid):
        """Возвращает данные пользователя по id.
        Если заходит гость, email, hash-password и id скрыты."""
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        user = user_service.get_one_guest(uid, token)
        try:
            res = user_schema.dump(user)
            return res, 200
        except Exception as e:
            print(e)
            return user, 200


@user_ns.route('/password')
class PasswordView(Resource):
    def put(self):
        """Принимает json-словарь вида:
        {'password_1': old password,
         'password_2': new password}"""
        token = request.headers['Authorization'].split('Bearer ')[-1]
        data = request.json
        user_service.update(token, data)
        return "", 201

