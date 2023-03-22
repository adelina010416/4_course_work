import calendar
import datetime

import jwt
from flask import abort

from constants import secret, algo
from implemented import user_service


class AuthService:
    def __init__(self, data):
        self.data = data

    def create(self):
        user_data = self.check_user()
        if not user_data:
            return {"error": "Неверные учётные данные"}, 401
        return self.generate_token(user_data)

    def update(self):
        try:
            data = jwt.decode(jwt=self.data, key=secret, algorithms=[algo])
        except Exception:
            abort(400)

        username = data['username']
        user = user_service.get_by_name(username)

        refresh_data = {'username': user.username, 'role': user.role}

        return self.generate_token(refresh_data)

    def check_user(self):
        """Проверяет по логину есть ли пользователь в БД и корректность пароля.
        Возвращает False, если хоть что-то неверно,
        или словарь с логином и ролью пользователя, если проверка прошла успешно."""
        user = user_service.get_by_name(self.data['username'])
        hash_password = user_service.get_hash(self.data['password'])

        if user is None or hash_password != user.password:
            return False
        return {'username': user.username, 'role': user.role}

    def generate_token(self, data):
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 201
