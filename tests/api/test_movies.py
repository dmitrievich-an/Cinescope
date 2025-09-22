from api.api_manager import ApiManager


class TestMovies:
    def test_get_all_movies(self, api_manager: ApiManager):
        response = api_manager.movie_api.get_movies()
        assert response.json()["movies"], "Афиши не получены"

    def test_get_movies_with_params(self, api_manager: ApiManager, query_params):
        response = api_manager.movie_api.get_movies(params=query_params)
        assert "movies" in response.json(), "Афиши не получены"

    def test_get_movie(self, api_manager: ApiManager, movie_id):
        response = api_manager.movie_api.get_movie_by_id(movie_id=14426)
        assert response.json()["id"], "Афиша не получена"

    def test_create_movie(self, authorized_api: ApiManager, movie_data):
        response = authorized_api.movie_api.create_movie(movie_data=movie_data, expected_status=[200, 201])
        assert response.json()["name"], "Фильм не создан"

    def test_delete_movie(self, authorized_api: ApiManager, temporary_movie):
        fix_movie_id = temporary_movie["id"]
        response = authorized_api.movie_api.delete_movie(movie_id=fix_movie_id, expected_status=[200, 201])
        assert response.json()["id"] == fix_movie_id, "В ответе отсутствует ID удаленного фильма"

        response = authorized_api.movie_api.delete_movie(movie_id=fix_movie_id, expected_status=404)
        assert response.json()["message"] == "Фильм не найден", "Текст ошибки не соответствует требованиям"

    def test_update_movie(self, authorized_api: ApiManager, temporary_movie, movie_data):
        response = authorized_api.movie_api.update_movie(
            movie_id=temporary_movie["id"],
            movie_data=movie_data,
            expected_status=[200, 201]
        )

        assert temporary_movie["id"] == response.json()["id"]
        assert movie_data["name"] == response.json()["name"]
