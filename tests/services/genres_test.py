import pytest
from unittest.mock import MagicMock
from dao.model.genre import Genre
from dao.genres_dao import GenreDAO
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    dao = GenreDAO(None)

    g1 = Genre(id=1, name='комедия')
    g2 = Genre(id=2, name='ужасы')
    g3 = Genre(id=3, name='вестерн')

    dao.get_one = MagicMock(return_value=g1)
    dao.get_all = MagicMock(return_value=[g1, g2, g3])
    dao.create = MagicMock(return_value=Genre(id=3))
    dao.delete = MagicMock(return_value=None)
    dao.update = MagicMock(return_value=Genre(id=3))

    return dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.service.get_one(1)
        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genre = self.service.get_all(1)
        assert len(genre) > 0

    def test_create(self):
        data = {'name': "романтика"}
        genre = self.service.create(data)
        assert genre.id is not None

    def test_update(self):
        data = {"id": 1, 'name': "романтика"}
        genre = self.service.update(data)
        assert genre.id is not None

    def test_delete(self):
        genre = self.service.delete(3)
        assert genre is None
