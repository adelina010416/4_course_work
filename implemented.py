from dao.directors_dao import DirectorDAO
from dao.genres_dao import GenreDAO
from dao.model.user import UserSchema
from dao.movies_dao import MovieDAO

from dao.model.director import DirectorSchema
from dao.model.genre import GenreSchema
from dao.model.movie import MovieSchema
from dao.users_dao import UserDAO

from service.director import DirectorService
from service.genre import GenreService
from service.movie import MovieService
from service.user import UserService
from setup_db import db

# подключение к ДАО
director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
user_dao = UserDAO(session=db.session)

# подключение сервисов
director_service = DirectorService(dao=director_dao)
genre_service = GenreService(dao=genre_dao)
movie_service = MovieService(dao=movie_dao)
user_service = UserService(dao=user_dao)

# подключение схем для сериализации
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
