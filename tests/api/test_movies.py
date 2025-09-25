import random

import pytest

from api.api_manager import ApiManager
from conftest import fake


class TestMovies:
    def test_get_all_movies(self, api_manager: ApiManager):
        response = api_manager.movie_api.get_movies()
        assert response.json()["movies"], "Афиши не получены"

    # def test_get_movies_with_params(self, api_manager: ApiManager, query_params):
    #     response = api_manager.movie_api.get_movies(params=query_params)
    #     assert "movies" in response.json(), "Афиши не получены"

    # @pytest.mark.parametrize(
    #     "min_price,max_price,genre_id",
    #     [
    #         (random.randint(1,400), random.randint(401,1000), random.randint(1,10)),
    #         (random.randint(1,400), random.randint(401,1000), random.randint(11,99)),
    #         (random.randint(9999,9999), random.randint(99999,99999), random.randint(1,10)),
    #         (random.randint(-10,-1), random.randint(401,1000), random.randint(1,10)),
    #         (random.randint(200,400), random.randint(100,199), random.randint(1,10)),
    #         ("abc", random.randint(401,1000), random.randint(1,10)),
    #     ],
    #     ids=["valid_params", "invalid_genre_id" ,"very_big_price", "negative_price", "min_price_over_max_price",
    #          "string_in_price"]
    # )
    @pytest.mark.parametrize(
        "min_price,max_price,genre_id",
        [
            (1, 1000, 2),
            (10, 400, 3),
            (500, 900, 5)
        ]
    )
    def test_get_movies_with_params(self, api_manager, min_price, max_price, genre_id):
        response = api_manager.movie_api.get_movies(
            params={
                "minPrice": min_price,
                "maxPrice": max_price,
                "genreId": genre_id
            }
        )
        assert "movies" in response.json(), "Афиши не получены"

    def test_get_movie(self, api_manager: ApiManager, movie_id):
        response = api_manager.movie_api.get_movie_by_id(movie_id=movie_id)
        assert response.json()["id"], "Афиша не получена"

    @pytest.mark.slow
    def test_create_movie(self, authorized_api: ApiManager, movie_data):
        response = authorized_api.movie_api.create_movie(movie_data=movie_data, expected_status=[200, 201])
        assert response.json()["name"], "Фильм не создан"

    @pytest.mark.slow
    def test_delete_movie(self, super_admin, temporary_movie):
        fix_movie_id = temporary_movie["id"]
        response = super_admin.api.movie_api.delete_movie(movie_id=fix_movie_id, expected_status=[200, 201])
        assert response.json()["id"] == fix_movie_id, "В ответе отсутствует ID удаленного фильма"

        response = super_admin.api.movie_api.delete_movie(movie_id=fix_movie_id, expected_status=404)
        assert response.json()["message"] == "Фильм не найден", "Текст ошибки не соответствует требованиям"

    def test_update_movie(self, authorized_api: ApiManager, temporary_movie, movie_data):
        response = authorized_api.movie_api.update_movie(
            movie_id=temporary_movie["id"],
            movie_data=movie_data,
            expected_status=[200, 201]
        )

        assert temporary_movie["id"] == response.json()["id"]
        assert movie_data["name"] == response.json()["name"]
