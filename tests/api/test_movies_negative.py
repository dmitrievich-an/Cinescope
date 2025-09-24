import random

from conftest import fake


class TestMoviesNegative:
    # GET:
    def test_get_movie_with_invalid_params(self, api_manager, invalid_query_params):
        response = api_manager.movie_api.get_movies(params=invalid_query_params, expected_status=400)
        assert response.json()["message"], "Отсутствует сообщение об ошибке"

    def test_get_movie_by_invalid_id(self, api_manager):
        invalid_id = random.randint(123456789, 987654321)
        response = api_manager.movie_api.get_movie_by_id(
            movie_id=invalid_id,
            expected_status=404
        )
        assert response.json()["message"], "Отсутствует сообщение об ошибке"

    # POST:
    def test_create_movie_with_invalid_data(self, super_admin, invalid_movie_data):
        response = super_admin.api.movie_api.create_movie(movie_data=invalid_movie_data, expected_status=400)
        assert response.json()["message"], "Отсутствует сообщение об ошибке"

    def test_create_movie_without_auth(self, api_manager_without_auth, movie_data):
        response = api_manager_without_auth.movie_api.create_movie(movie_data=movie_data, expected_status=401)
        assert response.json()["message"] == "Unauthorized", "Неверный текст об ошибке"

    def test_create_movie_without_access(self, common_user, movie_data):
        response = common_user.api.movie_api.create_movie(movie_data=movie_data, expected_status=403)
        assert response.json()["message"] == "Forbidden resource", "Неверный текст об ошибке"

    def test_create_movie_with_used_name(self, super_admin, movie_data, temporary_movie):
        movie_data_with_used_name = {**movie_data, "name": temporary_movie["name"]}

        response = super_admin.api.movie_api.create_movie(
            movie_data=movie_data_with_used_name,
            expected_status=409)
        assert response.json()["message"] == "Фильм с таким названием уже существует", "Неверный текст об ошибке"

    # DELETE:
    def test_delete_movie_without_auth(self, api_manager_without_auth, temporary_movie):
        response = api_manager_without_auth.movie_api.delete_movie(movie_id=temporary_movie["id"],
                                                                   expected_status=401)
        assert response.json()["message"] == "Unauthorized", "Неверный текст об ошибке"

    def test_delete_movie_without_access(self, common_user, temporary_movie):
        response = common_user.api.movie_api.delete_movie(movie_id=temporary_movie["id"],
                                                                   expected_status=403)
        assert response.json()["message"] == "Forbidden resource", "Неверный текст об ошибке"

    def test_delete_movie_with_invalid_id(self, super_admin):
        invalid_id = random.choice([fake.word(), random.randint(123456789, 987654321)])
        response = super_admin.api.movie_api.delete_movie(movie_id=invalid_id, expected_status=404)
        assert response.json()["message"], "Отсутствует сообщение об ошибке"

    def test_delete_movie_with_invalid_param(self, super_admin):
        invalid_id = f"{fake.word()}%EE{fake.word()}"  # некоторые URL-кодированные байты (%XX) ломают запрос
        response = super_admin.api.movie_api.delete_movie(movie_id=invalid_id, expected_status=400)
        assert response.json()["error"] == "Bad Request", "Отсутствует сообщение об ошибке"

    # PATCH:
    def test_update_movie_with_invalid_data(self, authorized_api, temporary_movie, invalid_movie_data):
        response = authorized_api.movie_api.update_movie(
            movie_id=temporary_movie["id"],
            movie_data=invalid_movie_data,
            expected_status=400
        )
        assert response.json()["message"], "Отсутствует сообщение об ошибке"

    def test_update_movie_without_auth(self, api_manager_without_auth, temporary_movie, movie_data):
        response = api_manager_without_auth.movie_api.update_movie(
            movie_id=temporary_movie["id"],
            movie_data=movie_data,
            expected_status=401
        )
        assert response.json()["message"] == "Unauthorized", "Неверный текст об ошибке"

    def test_update_movie_with_invalid_id(self, authorized_api, movie_data):
        invalid_id = random.choice([fake.word(), random.randint(123456789, 987654321)])
        response = authorized_api.movie_api.update_movie(
            movie_id=invalid_id,
            movie_data=movie_data,
            expected_status=404)
        assert response.json()["message"], "Отсутствует сообщение об ошибке"
