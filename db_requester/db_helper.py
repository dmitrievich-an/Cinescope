from sqlalchemy.orm import Session

from db_models.movies import MovieDBModel
from db_models.user import UserDBModel


class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    """Класс с методами для работы с БД в тестах"""

    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Создает тестового пользователя"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    """Методы для user"""

    def get_user_by_id(self, user_id: str):
        """Получает пользователя по id"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, user_email: str):
        """Получает пользователя по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == user_email).first()

    def user_exists_by_email(self, user_email: str):
        """Проверяет существование юзера по его email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == user_email).count() > 0

    def delete_user(self, user: UserDBModel):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self, object_to_delete: list):
        """Очищает тестовые данные"""
        for obj in object_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    """Методы для movies"""

    def get_movie_by_id(self, movie_id: str):
        """Получает фильм по ID"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

    def get_movie_by_name(self, movie_name: str):
        """Получает фильм по названию"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name).first()

    def movie_exists_by_name(self, movie_name: str):
        """Проверяет существование фильма по его названию"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name).count() > 0

    def create_test_movie(self, movie_data: dict):
        """Принимает словарь и создает тестовый фильм"""
        movie = MovieDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    # Получение первого фильма, чтобы в дальнейшем взять его id или имя
    def get_first_movie(self):
        """Получает существующий (первый) фильм"""
        first_movie = self.db_session.query(MovieDBModel).first()
        return first_movie
