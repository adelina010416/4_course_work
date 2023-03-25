import jwt
from flask_restx import abort

from constants import secret, algo
from dao.favorite_dao import FavoriteDAO
from service.user import UserService


class FavoriteService:
    def __init__(self, dao: FavoriteDAO, service: UserService):
        self.dao = dao
        self.service = service

    def create(self, data, mid):
        user_id = self.get_user_id(data)
        new_data = {"user_id": user_id, "movie_id": mid}

        return self.dao.create(new_data)

    def delete(self, data, mid):
        user_id = self.get_user_id(data)
        self.dao.delete(mid, user_id)

    def get_user_id(self, data):
        token = data.split('Bearer ')[-1]
        try:
            user_data = jwt.decode(token, secret, algorithms=[algo])
            user = self.service.get_by_name(user_data.get("email"))
            return user.id
        except Exception:
            abort(400)
