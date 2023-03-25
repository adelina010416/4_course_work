from flask import request
from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError

from dao.model.genre import GenreSchema
from decorators import auth_required, admin_required
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        page = request.args.get("page")
        rs = genre_service.get_all(page)
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        try:
            genre_service.create(data)
        except IntegrityError:
            return "This genre is already used. Please, try again."
        return "", 201

    @admin_required
    def put(self):
        data = request.json
        genre_service.update(data)
        return "", 204


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def delete(self, rid):
        genre_service.delete(rid)
        return "", 204
