from marshmallow import Schema, fields

from setup_db import db
from dao.model.genre import Genre


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre = db.Column(db.String, db.ForeignKey("genre.name"))
    genre = db.relationship("Genre")


class UserSchema(Schema):
    __tablename__ = 'user'
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()
    role = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()
