import os
import sqlite3

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from logger import get_logger
from postgres_saver import PostgresSaver
from sqlite_extractor import SQLiteLoader
from utils import get_models, get_db_creds


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Upload data method from SQLite to Postgres
    Args:
        connection: connection to SQLite
        pg_conn: connection to PostgreSQL
    """

    for table_name, table_model in models.items():
        sqlite_loader = SQLiteLoader(connection, table_name, table_model, PAGE_SIZE)
        data_from_sql = sqlite_loader.extract_movies()

        postgres_saver = PostgresSaver(pg_conn, table_name, table_model, PAGE_SIZE)
        postgres_saver.save_all_data(data_from_sql)

    logger.info('Loading data from SQLite DB to PostgreSQL DB completed successfully!')


if __name__ == '__main__':
    # upload environment variables
    load_dotenv()

    # convert type of PAGE_SIZE from str to int
    PAGE_SIZE = int(os.environ.get('PAGE_SIZE'))

    logger = get_logger(__name__)

    # databases creds
    db_creds = get_db_creds()

    # get all models
    models = get_models()

    # connection to DBs
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**db_creds['psql'], cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

    # close connections
    sqlite_conn.close()
    pg_conn.close()
