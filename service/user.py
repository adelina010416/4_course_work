import hashlib

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.users_dao import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_name(self, username):
        return self.dao.get_by_login(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.get_hash(user_d["password"])
        return self.dao.create(user_d)

    def update(self, user_d):
        return self.dao.update(user_d)

    def get_hash(self, password):
        """Получает пароль, возвращает хэш"""
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")
        return hash_password
