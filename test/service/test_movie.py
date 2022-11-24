from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_1 = Movie(id=1, title='movie_1', description='description_1', trailer='trailer_1', year=2007, rating=9.0, genre_id=1, director_id=5)
    movie_2 = Movie(id=2, title='movie_2', description='description_2', trailer='trailer_2', year=1998, rating=6.7, genre_id=3, director_id=4)
    movie_3 = Movie(id=3, title='movie_3', description='description_3', trailer='trailer_3', year=2022, rating=9.2, genre_id=5, director_id=3)
    movie_4 = Movie(id=4, title='movie_4', description='description_4', trailer='trailer_4', year=2012, rating=3.5, genre_id=4, director_id=2)
    movie_5 = Movie(id=5, title='movie_5', description='description_5', trailer='trailer_5', year=2000, rating=8.1, genre_id=2, director_id=1)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_5, movie_4, movie_3, movie_2, movie_1])
    movie_dao.create = MagicMock(return_value=Movie(id=6))
    movie_dao.delete = MagicMock(return_value=Movie(id=3))
    movie_dao.update = MagicMock(return_value=movie_3)

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None
        assert movie.title == 'movie_1'

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0
        assert len(movies) == 5

    def test_create(self):
        data = {
            "id": 6,
            "title": 'movie_6',
            "description": 'description_6',
            "trailer": 'trailer_6',
            "year": 2001,
            "rating": 6.1,
            "genre_id": 4,
            "director_id": 2
        }

        movie = self.movie_service.create(data)

        assert movie.id is not None
        assert movie.id == 6

    def test_delete(self):
        movie = self.movie_service.delete(3)

        assert movie is None

    def test_update(self):
        data = {
            "id": 6,
            "title": 'movie_6',
            "description": 'description_6',
            "trailer": 'trailer_6',
            "year": 2001,
            "rating": 6.1,
            "genre_id": 4,
            "director_id": 2
        }

        movie = self.movie_service.update(data)

        assert movie.id is not None

    def test_partially_update(self):
        data = {
            "id": 6,
            "trailer": 'trailer_6',
            "year": 2001,
            "rating": 6.1
        }

        movie = self.movie_service.partially_update(data)

        assert movie is None
