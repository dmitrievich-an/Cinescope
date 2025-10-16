import os

from dotenv import load_dotenv

load_dotenv()


class DBMoviesCreds:
    USERNAME = os.getenv("DB_MOVIES_USERNAME")
    PASSWORD = os.getenv("DB_MOVIES_PASSWORD")
    HOST = os.getenv("DB_MOVIES_HOST")
    PORT = os.getenv("DB_MOVIES_PORT")
    DATABASE_NAME = os.getenv("DB_MOVIES_NAME")
