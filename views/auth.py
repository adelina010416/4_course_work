from flask import request, abort
from flask_restx import Resource, Namespace

from service.auth import AuthService

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        data = request.json
        username = data.get('username', None)
        password = data.get('password', None)
        if None in [username, password]:
            abort(400)

        return AuthService(data).create()

    def put(self):
        data = request.json
        token = data.get('refresh_token')
        if token is None:
            abort(400)

        return AuthService(token).update()
