import hashlib

import jwt
from flask_restx import abort

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, secret, algo
from dao.users_dao import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one_guest(self, uid, token):
        user = self.dao.get_one(uid)
        is_owner = self.check_email_by_token(user, token)
        if is_owner:
            return user
        return {"name": user.name,
                "surname": user.surname,
                "role": user.role,
                "favorite_genre": user.favorite_genre
                }

    def get_one_owner(self, token):
        try:
            user_guest = jwt.decode(token, secret, algorithms=[algo])
            email = user_guest.get('email')
            return self.dao.get_by_email(email)
        except Exception:
            abort(400)

    def get_by_name(self, email):
        return self.dao.get_by_email(email)

    def get_all(self):
        return self.dao.get_all()

    def update(self, token, data):
        try:
            user_guest = jwt.decode(token, secret, algorithms=[algo])
        except Exception:
            abort(400)
        email = user_guest.get('email')
        user = self.dao.get_by_email(email)
        old_password = data.get("password_1")
        new_password = data.get("password_2")
        hash_old_password = self.get_hash(old_password)

        if hash_old_password != user.password:
            abort(403)

        user.password = self.get_hash(new_password)
        return self.dao.update(user)

    def partially_update(self, token, data):
        try:
            user_guest = jwt.decode(token, secret, algorithms=[algo])
        except Exception:
            abort(400)
        email = user_guest.get('email')
        user = self.dao.get_by_email(email)
        if "name" in data:
            user.name = data["name"]
        if "surname" in data:
            user.surname = data["surname"]
        if "favorite_genre" in data:
            user.favorite_genre = data["favorite_genre"]
        self.dao.update(user)

    def get_hash(self, password):
        """Получает пароль, возвращает хэш"""
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")
        return hash_password

    def check_email_by_token(self, user, token):
        """Сравнивает email из полученного токена и email запрошенной страницы.
        Если email совпадает, возвращает все данные пользователя.
        Иначе - возвращает False."""
        try:
            user_guest = jwt.decode(token, secret, algorithms=[algo])
        except Exception:
            abort(400)
        if user.email == user_guest.get('email'):
            return user
        return False
