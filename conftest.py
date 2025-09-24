import copy
import random

import pytest
import requests
from faker import Faker

from api.api_manager import ApiManager
from constants.constants import LOCATIONS, ADMIN_CREDS
from constants.roles import Roles
from entities.user import User
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator

fake = Faker()


@pytest.fixture
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()
    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture
def movie_data():
    random_movie_name = DataGenerator.generate_random_movie_name()
    return {
        "name": random_movie_name,
        "imageUrl": "https://image.url",
        "price": fake.random_int(min=100, max=1000, step=50),
        "description": fake.text(max_nb_chars=100),
        "location": random.choice(LOCATIONS),
        "published": fake.boolean(),
        "genreId": fake.random_int(min=1, max=10)
    }


@pytest.fixture
def movie_id(api_manager):
    response = api_manager.movie_api.get_movies()
    response_data = response.json()
    movie_id = response_data["movies"][0]["id"]
    return movie_id


@pytest.fixture
def temporary_movie(authorized_api, movie_data):
    """
    Фикстура для создания нового фильма на время теста.
    """
    response = authorized_api.movie_api.create_movie(movie_data=movie_data)
    temporary_movie = response.json()
    yield temporary_movie
    authorized_api.movie_api.delete_movie(movie_id=temporary_movie["id"], expected_status=[200, 404])


@pytest.fixture
def query_params():
    return {
        "pageSize": random.randint(1, 11),
        "page": random.choice([1, 2]),
        "minPrice": random.randint(1, 50),
        "maxPrice": random.randint(100, 1000),
        "locations": random.sample(LOCATIONS, k=random.randint(1, len(LOCATIONS))),
        "published": random.choice([True, False]),
        "genreId": random.randint(1, 10),
        "createdAt": random.choice(["asc", "desc"])
    }


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def session_without_auth():
    """
    Фикстура для создания HTTP-сессии без дальнейшей авторизации.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture(scope="session")
def api_manager_without_auth(session_without_auth):
    """
    Фикстура для создания экземпляра ApiManager без дальнейшей авторизации.
    """
    return ApiManager(session_without_auth)


@pytest.fixture(scope="session")
def authorized_api(api_manager):
    """
    Фикстура, которая авторизуется под админом и обновляет заголовки для всех запросов.
    Возвращает api_manager с готовыми заголовками.
    """
    api_manager.auth_api.authenticate(ADMIN_CREDS)
    return api_manager


@pytest.fixture(
    params=[
        {"genreId": fake.word()},
        {"page": fake.word()},
        {"minPrice": random.randint(a=1, b=1000) * (-1)},
        {"minPrice": random.randint(a=500, b=1000), "maxPrice": random.randint(a=1, b=499)},
        {"locations": random.randint(a=0, b=100)},
        {"pageSize": random.randint(a=21, b=99)},
        {"createdAt": fake.word()}
    ]
)
def invalid_query_params(request):
    """
    Параметризированная фикстура для некорректных GET-запросов
    """
    return request.param


@pytest.fixture(
    params=[
        pytest.param(("price", fake.word()), id="price_not_number"),
        pytest.param(("genreId", fake.word()), id="invalid_genre"),
        pytest.param(("location", ""), id="empty_location"),
        pytest.param(("published", random.randint(a=2, b=100)), id="published_not_bool"),
    ]
)
def invalid_movie_data(movie_data, request):
    """
    Параметризированная фикстура для некорректного тела запроса
    """
    invalid_data = copy.deepcopy(movie_data)
    key, bad_value = request.param
    invalid_data[key] = bad_value
    return invalid_data

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user