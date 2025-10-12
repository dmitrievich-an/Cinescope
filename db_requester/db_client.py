from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from resources.db_creds import DBMoviesCreds

db_creds = DBMoviesCreds()

DBNAME = db_creds.DATABASE_NAME
USERNAME = db_creds.USERNAME
PASSWORD = db_creds.PASSWORD
HOST = db_creds.HOST
PORT = db_creds.PORT

# движок для подключения к БД
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}",
    echo=False  # Если нужна отладка, то ставим True
)

# создаем фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False,  # изменения не сохраняются автоматически (нужно вызывать commit())
    autoflush=False,  # не отправлять запросы в БД до commit()
    bind=engine  # связывает сессию с конкретным engine (соединением с БД)
)


def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()
