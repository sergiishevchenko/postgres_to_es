import os

from dotenv import load_dotenv
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


def get_db_creds():
    load_dotenv()
    db_creds = {
        'psql': {
            'dbname': os.environ.get('DB_NAME'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST'),
            'port': os.environ.get('DB_PORT')
        },
        'sqlite': {
            'db_path': os.environ.get('sqlite_DB_NAME')
        }
    }
    return db_creds


def get_models():
    models = {
        'film_work': FilmWork,
        'genre': Genre,
        'genre_film_work': GenreFilmWork,
        'person': Person,
        'person_film_work': PersonFilmWork
    }
    return models


def get_sqlite_data():
    test_sqlite_data = {'created_at': 'substr(created_at,0,20)',
                        'updated_at': 'substr(updated_at,0,20)'
                        }
    return test_sqlite_data


def get_postgres_data():
    test_postgres_data = {'created_at': 'TO_CHAR(created_at,\'YYYY-MM-DD HH24:MI:SS\')',
                          'updated_at': 'TO_CHAR(updated_at,\'YYYY-MM-DD HH24:MI:SS\')',
                          }
    return test_postgres_data
