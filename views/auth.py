from flask import request, abort
from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        """Вход в личный аккаунт"""
        data = request.json
        email = data.get('email', None)
        password = data.get('password', None)

        if None in [email, password]:
            abort(400)

        return auth_service.create_login(data)

    def put(self):
        """Получение новой пары токенов"""
        data = request.json
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        print(access_token)
        print(refresh_token)

        if None in [access_token, refresh_token]:
            abort(400)

        return auth_service.update(access_token, refresh_token)


@auth_ns.route('/register')
class AuthView2(Resource):
    def post(self):
        """Регистрация нового пользователя"""
        data = request.json

        try:
            auth_service.create(data)
            return "", 201

        except IntegrityError:
            return "This e-mail is already used. Please, try again."
