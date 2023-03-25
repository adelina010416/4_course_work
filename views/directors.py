from flask import request
from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError

from dao.model.director import DirectorSchema
from decorators import auth_required, admin_required
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        pages = request.args.get("page")
        rs = director_service.get_all(pages)
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        try:
            director_service.create(data)
        except IntegrityError:
            return "This genre is already used. Please, try again."
        return "", 201

    @admin_required
    def put(self):
        data = request.json
        director_service.update(data)
        return "", 204


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def delete(self, rid):
        director_service.delete(rid)
        return "", 204
