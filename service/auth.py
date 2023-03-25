import calendar
import datetime

import jwt
from flask import abort

from constants import secret, algo
from service.user import UserService
from dao.auth_dao import AuthDAO


class AuthService:
    def __init__(self, dao: AuthDAO, user_service: UserService):
        self.user_service = user_service
        self.dao = dao

    def create_register(self, data):
        """Регистрация нового пользователя"""
        data["password"] = self.user_service.get_hash(data["password"])
        return self.dao.create(data)

    def create_login(self, data):
        """Вход в личный аккаунт"""
        user_data = self.check_user(data)
        if not user_data:
            return {"error": "Неверные учётные данные"}, 401
        return self.generate_token(user_data)

    def update(self, a_token, r_token):
        try:
            a_token = jwt.decode(jwt=a_token, key=secret, algorithms=[algo])
            r_token = jwt.decode(jwt=r_token, key=secret, algorithms=[algo])
        except Exception:
            abort(400)

        email = r_token['email']
        user = self.user_service.get_by_name(email)

        refresh_data = {'email': user.email, 'role': user.role}

        return self.generate_token(refresh_data)

    def check_user(self, data):
        """Проверяет по логину есть ли пользователь в БД и корректность пароля.
        Возвращает False, если хоть что-то неверно,
        или словарь с логином и ролью пользователя, если проверка прошла успешно."""

        user = self.user_service.get_by_name(data['email'])
        hash_password = self.user_service.get_hash(data['password'])

        if user is None or hash_password != user.password:
            return False
        return {'email': user.email, 'role': user.role}

    def generate_token(self, data):
        """Генерирует пару токенов: access_token and refresh_token"""

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 201
