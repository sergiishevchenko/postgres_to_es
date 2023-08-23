import sqlite3
import psycopg2

from contextlib import contextmanager
from dotenv import load_dotenv
from dataclasses import fields
from psycopg2.extras import DictCursor
from utils import get_db_creds, get_models, get_postgres_data, get_sqlite_data


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def test_tables_data_integrity():
    '''Data integrity checking between each pair of tables in SQLite and Postgres.
       It is enough to check the number of records in each table.
    '''

    # call method for getting list of models
    models = get_models()

    # call method for getting databases creds
    db_creds = get_db_creds()

    # Connection to PostgreSQL and SQLite DBs
    with (conn_context(**db_creds['sqlite']) as sqlite_conn, psycopg2.connect(**db_creds['psql'], cursor_factory=DictCursor) as pg_conn):
        for table_name in models:
            curs = sqlite_conn.cursor()
            # count rows in SQLite DB
            sqlite_rows_quantity = curs.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()[0]

            cursor = pg_conn.cursor()
            # count rows in PostgreSQL DB
            cursor.execute(f'SELECT COUNT(*) FROM content.{table_name};')

            # compare rows quantity
            postgres_rows_quantity = cursor.fetchone()[0]

            assert sqlite_rows_quantity == postgres_rows_quantity, \
                (f'Record quantity in {table_name} PostgreSQL does not equal to SQLite.')


def test_table_records_content():
    '''Checking the contents of records within each table.'''

    # call method for getting list of models
    models = get_models()

    # call method for getting databases creds
    db_creds = get_db_creds()

    # call the methods for getting test data
    sqlite_data = get_sqlite_data()
    postgres_data = get_postgres_data()

    # Connection to PostgreSQL and SQLite DBs
    with (conn_context(**db_creds['sqlite']) as sqlite_conn, psycopg2.connect(**db_creds['psql'], cursor_factory=DictCursor) as pg_conn):

        for table_name in models:
            field_names_list = [
                field.name for field in fields(models[table_name])]

            sqlite_fields = [
                sqlite_data[field] if field in sqlite_data else field for field in field_names_list]
            sqlite_field_to_str = ','.join(sqlite_fields)
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_field_data = sqlite_cursor.execute(
                f"SELECT {sqlite_field_to_str} FROM {table_name}").fetchall()

            postgres_fields = [
                postgres_data[field] if field in postgres_data else field for field in field_names_list]
            postgres_field_to_str = ','.join(postgres_fields)
            postgres_cursor = pg_conn.cursor()
            postgres_field_data = postgres_cursor.execute(
                f"SELECT {postgres_field_to_str} FROM content.{table_name}").fetchall()

            for i in range(len(postgres_field_data)):
                assert len(set(postgres_field_data[i]) - set(tuple(
                    sqlite_field_data[i]))) == 0, (f'Names are not the same in table {table_name}')


if __name__ == '__main__':
    # upload environment variables
    load_dotenv()

    # Tests
    # call the method for checking data integrity
    test_tables_data_integrity()
    # call the method for checking the contents of records within each table
    test_table_records_content()