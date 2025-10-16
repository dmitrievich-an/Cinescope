import allure
from sqlalchemy.orm import Session

from constants.constants import BASE_URL_API, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from db_models.accounts_transaction_template import AccountTransactionTemplate


class MovieAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_API)

    def get_movies(self, params=None, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

    def get_movie_by_id(self, expected_status=200, movie_id=None):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=None):
        if expected_status is None:
            expected_status = [200, 201]
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, expected_status=None, movie_id=None):
        if expected_status is None:
            expected_status = [200, 201]

        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def update_movie(self, movie_data, movie_id=None, expected_status=None):
        if expected_status is None:
            expected_status = [200, 201]

        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=movie_data,
            expected_status=expected_status
        )

    @staticmethod
    @allure.step("Функция перевода денег: transfer_money")
    @allure.description("""
                функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
                и вызывая метод transfer_money, мы как будто бы делаем запрос в api_manager.movies_api.transfer_money
                """)
    def transfer_money(session: Session, from_account, to_account, amount):
        """
        Транзакция перевода денег с одного баланса на другой
        :param session: Сессия SQLAlchemy
        :param from_account: откуда списываем деньги
        :param to_account: куда зачисляем
        :param amount: сколько переводим
        """

        with allure.step(" Получаем счета"):
            from_account = (
                session.query(AccountTransactionTemplate)
                .filter(AccountTransactionTemplate.user == from_account.user)  # filter принимает логические выражения
                .one()
            )
            to_account = (
                session.query(AccountTransactionTemplate)
                .filter_by(user=to_account.user)  # filter_by принимает именованные аргументы
                .one()
            )

        with allure.step("Проверяем, что на счете достаточно средств"):
            if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете отправителя")

        with allure.step("Выполняем перевод"):
            from_account.balance -= amount
            to_account.balance += amount

        with allure.step("Сохраняем изменения"):
            session.commit()
