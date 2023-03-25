from unittest.mock import MagicMock

import pytest

from dao.directors_dao import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    dao = DirectorDAO(None)

    d1 = Director(id=1, name='Иван')
    d2 = Director(id=2, name='Петр')
    d3 = Director(id=3, name='Вася')

    dao.get_one = MagicMock(return_value=d1)
    dao.get_all = MagicMock(return_value=[d1, d2, d3])
    dao.create = MagicMock(return_value=Director(id=3))
    dao.delete = MagicMock(return_value=None)
    dao.update = MagicMock(return_value=Director(id=3))

    return dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.service.get_one(1)
        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.service.get_all(1)
        assert len(directors) > 0

    def test_create(self):
        data = {'name': "Игорь"}
        director = self.service.create(data)
        assert director.id is not None

    def test_update(self):
        data = {"id": 1, 'name': "Игорь"}
        director = self.service.update(data)
        assert director.id is not None

    def test_delete(self):
        director = self.service.delete(3)
        assert director is None
