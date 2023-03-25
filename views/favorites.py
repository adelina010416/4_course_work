from flask import request
from flask_restx import Resource, Namespace

from implemented import favorite_service
from decorators import auth_required

favorite_ns = Namespace('favorites')


@favorite_ns.route('/movies/<int:mid>')
class FavoriteView(Resource):
    @auth_required
    def post(self, mid):
        data = request.headers['Authorization']
        favorite_service.create(data, mid)
        return "", 201

    @auth_required
    def delete(self, mid):
        data = request.headers['Authorization']
        favorite_service.delete(data, mid)
        return "", 204
