from contextlib import contextmanager

from elasticsearch import Elasticsearch
import psycopg2
from psycopg2.extras import RealDictCursor


@contextmanager
def connection_to_psql(database: dict):
    conn_to_psql = psycopg2.connect(**database, cursor_factory=RealDictCursor)
    conn_to_psql.set_session(autocommit=True)

    try:
        yield conn_to_psql
    finally:
        conn_to_psql.close()


@contextmanager
def connection_to_els(database: str):
    conn_to_els = Elasticsearch(database)

    try:
        yield conn_to_els
    finally:
        conn_to_els.close()
