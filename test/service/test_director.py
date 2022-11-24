from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService


@pytest.fixture()
def directors_dao():
    directors_dao = DirectorDAO(None)

    director_1 = Director(id=1, name='Квентин Тарантино')
    director_2 = Director(id=2, name='Алексей Балабанов')
    director_3 = Director(id=3, name='Никита Михалков')
    director_4 = Director(id=4, name='Тим Бёртон')
    director_5 = Director(id=5, name='Ридли Скотт')

    directors_dao.get_one = MagicMock(return_value=director_1)
    directors_dao.get_all = MagicMock(return_value=[director_5, director_4, director_3, director_2, director_1])
    directors_dao.create = MagicMock(return_value=Director(id=6))
    directors_dao.delete = MagicMock(return_value=Director(id=3))
    directors_dao.update = MagicMock(return_value=director_3)

    return directors_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, directors_dao):
        self.director_service = DirectorService(dao=directors_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None
        assert director.name == 'Квентин Тарантино'

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) > 0
        assert len(directors) == 5

    def test_create(self):
        data = {
            "name": 'Питер Аванзино'
        }

        director = self.director_service.create(data)

        assert director.id is not None
        assert director.id == 6

    def test_delete(self):
        director = self.director_service.delete(3)

        assert director is None

    def test_update(self):
        data = {
            "id": 3,
            "name": 'Питер Аванзино'
        }

        director = self.director_service.update(data)

        assert director.id is not None

    def test_partially_update(self):
        data = {
            "id": 3,
            "name": 'Питер Аванзино'
        }

        director = self.director_service.partially_update(data)

        assert director is None
