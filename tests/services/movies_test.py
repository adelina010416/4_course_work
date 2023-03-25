import pytest
from unittest.mock import MagicMock
from dao.model.movie import Movie
from dao.movies_dao import MovieDAO
from service.movie import MovieService
from setup_db import db


@pytest.fixture()
def movie_dao():
    dao = MovieDAO(db.session)

    m1 = Movie(id=1,
               title='Парфюмер',
               description='блаблабла',
               trailer='бла',
               year=2015,
               rating=2.3,
               genre_id=1,
               director_id=1)
    m2 = Movie(id=2,
               title='Ведьма',
               description='блаблабла',
               trailer='бла',
               year=2018,
               rating=6.3,
               genre_id=2,
               director_id=2)
    m3 = Movie(id=3,
               title='Мстители',
               description='бред умственноотсталого',
               trailer='бла',
               year=2019,
               rating=1.1,
               genre_id=3,
               director_id=3)

    dao.get_one = MagicMock(return_value=m1)
    dao.get_all = MagicMock(return_value=[m1, m2, m3])
    dao.create = MagicMock(return_value=Movie(id=4, title="Mirrors"))
    dao.delete = MagicMock(return_value=None)
    dao.update = MagicMock(return_value=None)

    return dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.service.get_one(1)
        assert movie is not None
        assert movie.id == 1
        assert movie.title == "Парфюмер"

    def test_get_all(self):
        movie = self.service.get_all(1)
        assert len(movie) > 0
        assert len(movie) == 3

    def test_create(self):
        data = {"title": 'Зеркала',
                "description": 'мужик смотрит в зеркала',
                "trailer": 'вау, какие зеркала',
                "year": 2019,
                "rating": 9.9,
                "genre_id": 3,
                "director_id": 3}
        movie = self.service.create(data)
        assert movie.id == 4
        assert movie.title == "Mirrors"

    def test_update(self):
        data = {"title": 'Зеркала',
                "description": 'мужик смотрит в зеркала',
                "trailer": 'вау, какие зеркала',
                "year": 2019,
                "rating": 9.9,
                "genre_id": 3,
                "director_id": 3}
        movie = self.service.update(data)
        assert movie is None

    def test_delete(self):
        movie = self.service.delete(3)
        assert movie is None
