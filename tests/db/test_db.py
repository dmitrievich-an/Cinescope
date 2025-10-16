import uuid
from datetime import datetime

import allure
import pytest
from sqlalchemy.orm import Session

from api.api_manager import ApiManager
from conftest import api_manager
from constants.locarions import Locations
from db_models.accounts_transaction_template import AccountTransactionTemplate
from db_models.movies import MovieDBModel
from utils.data_generator import DataGenerator


class TestDataBase:

    def test_db_requests(self, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")

    def test_crud_movie(self, db_helper, super_admin):
        movie_name = DataGenerator.generate_random_movie_name()

        movie = MovieDBModel(
            name=f"{movie_name} 2",
            price=500,
            description="A mind-bending thriller by Christopher Nolan.",
            image_url="https://example.com/inception.jpg",
            location=Locations.MSK,
            published=True,
            rating=3.6,
            genre_id=1,
            created_at=datetime.now()
        ).to_dict()

        # Существующий фильм
        existing_film = db_helper.get_first_movie().name

        # Проверяем, что создаваемого фильма не существует
        assert not db_helper.movie_exists_by_name(movie["name"]), f"Найден фильм с названием '{movie["name"]}'"

        # Создаем фильм
        test_movie = db_helper.create_test_movie(movie)

        # Проверяем, что фильм можно найти по названию
        assert db_helper.movie_exists_by_name(test_movie.name), f"Фильм с названием '{test_movie.name}' не найден"

        # Удаляем через апи
        super_admin.api.movie_api.delete_movie(movie_id=test_movie.id)

        # Проверяем, что фильм нельзя найти по названию
        assert not db_helper.movie_exists_by_name(test_movie.name), \
            f"Фильм с названием '{test_movie.name}' найден после удаления через API"

@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:
    @allure.story("Корректность перевода между двумя счетами")
    @allure.description("""
        Этот тест проверяет корректность перевода денег между двумя счетами.
        Шаги:
        1. Создание двух счетов: Stan и Bob.
        2. Перевод 200 единиц от Stan к Bob.
        3. Проверка изменения балансов.
        4. Очистка тестовых данных.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Artem Dmitrievich")
    @allure.title("Тест перевода 200 шекелей между счетами")
    def test_accounts_transaction_template(self, db_session: Session, api_manager: ApiManager):
        # Подготовка к тесту
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(user=f"Stan_{uuid.uuid4()}", balance=1000)
            bob = AccountTransactionTemplate(user=f"Bob_{uuid.uuid4()}", balance=500)
            db_session.add_all([stan, bob])
            db_session.commit()

        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Выполняем перевод 200 шекелей от stan к bob"):
                api_manager.movie_api.transfer_money(db_session, stan, bob, 200)

            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:
            with allure.step("ОШИБКА - откат транзакции"):
                db_session.rollback()

            pytest.fail(f"Ошибка при переводе денег: {e}")
        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()
