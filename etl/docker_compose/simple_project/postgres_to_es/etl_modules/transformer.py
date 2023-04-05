import json


class DataTransform:
    '''Класс DataTransform предназначен для обработки данных из PostgreSQL для загрузки в Elasticsearch.'''

    def transform_filmworks(self, transformed_filmworks: dict) -> list[dict]:
        transformed_filmworks = []
        for record in transformed_filmworks:
            filmwork = {
                'id': record['id'],
                'imdb_rating': record['imdb_rating'],
                'genre': record['genre'],
                'title': record['title'],
                'description': record['description'],
                'director': record['director'],
                'actors_names': record['actors_names'] if record['actors_names'] is not None else '',
                'writers_names': record['writers_names'] if record['writers_names'] is not None else '',
                'actors': json.loads(record['actors']) if record['actors'] is not None else [],
                'writers': json.loads(record['writers']) if record['writers'] is not None else []
            }
            transformed_filmworks.append(filmwork)
        return transformed_filmworks