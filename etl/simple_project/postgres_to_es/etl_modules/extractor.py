import datetime
from typing import Iterator

from utils.connection_to_db import connection_to_psql


class PostgresExtractor:
    '''Класс PostgresExtractor предназначен для извлечения данных из PostgreSQL'''

    def __init__(self, psql, page_size: int, storage_state, logger) -> None:
        self.page_size = page_size
        self.storage_state = storage_state
        self.database = psql
        self.logger = logger

    def extract_filmworks(self, extract_timestamp: datetime.datetime, start_timestamp: datetime.datetime, exclude_filmworks: list) -> Iterator:

        with connection_to_psql(self.database) as pg_conn, pg_conn.cursor() as cursor:
            sql = f"""
                    SELECT
                        fw.id,
                        fw.rating as imdb_rating,
                        json_agg(DISTINCT g.name) as genre,
                        fw.title,
                        fw.description,
                        string_agg(DISTINCT CASE WHEN pfw.role = 'director' THEN p.full_name ELSE '' END, ',') AS director,
                        array_remove(COALESCE(array_agg(DISTINCT CASE WHEN pfw.role = 'actor' THEN p.full_name END) FILTER (WHERE p.full_name IS NOT NULL)), NULL) AS actors_names,
                        array_remove(COALESCE(array_agg(DISTINCT CASE WHEN pfw.role = 'writer' THEN p.full_name END) FILTER (WHERE p.full_name IS NOT NULL)), NULL) AS writers_names,
                        concat('[', string_agg(DISTINCT CASE WHEN pfw.role = 'actor' THEN json_build_object('id', p.id, 'name', p.full_name) #>> '{{}}' END, ','), ']') AS actors,
                        concat('[', string_agg(DISTINCT CASE WHEN pfw.role = 'writer' THEN json_build_object('id', p.id, 'name', p.full_name) #>> '{{}}' END, ','), ']') AS writers,
                        GREATEST(MAX(fw.modified), MAX(g.modified), MAX(p.modified)) AS last_modified
                    FROM
                        content.film_work as fw
                        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                        LEFT JOIN content.person p ON p.id = pfw.person_id
                        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                        LEFT JOIN content.genre g ON g.id = gfw.genre_id
                    GROUP BY fw.id
                    """

            if exclude_filmworks:
                sql += f"""AND (fw.id not in {tuple(exclude_filmworks)} OR GREATEST(MAX(fw.modified), MAX(g.modified), MAX(p.modified)) > '{str(start_timestamp)}')"""
            sql += f"""HAVING GREATEST(MAX(fw.modified), MAX(g.modified), MAX(p.modified)) > '{str(extract_timestamp)}' ORDER BY GREATEST(MAX(fw.modified), MAX(g.modified), MAX(p.modified)) DESC;"""
            cursor.execute(sql)

            while True:
                rows = cursor.fetchmany(self.page_size)
                if not rows:
                    self.logger.info('There are no required rows.')
                    break
                for data in rows:
                    self.logger.info('There are required rows.')
                    ids_list = self.storage_state.get_state('filmworks')
                    ids_list.append(data['id'])
                    self.storage_state.set_state('filmworks', ids_list)
                yield rows
