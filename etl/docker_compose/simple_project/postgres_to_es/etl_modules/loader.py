import elasticsearch
from elasticsearch.exceptions import ConnectionError, helpers
from utils.connection_to_db import connection_to_els
from utils.backoff import backoff


class ElasticsearchLoader:
    '''Класс ElasticsearchLoader предназначен для загрузки данных в Elasticsearch.'''

    def __init__(self, database, logger) -> None:
        self.database = database
        self.logger = logger
        self.create_index('movies')

    @backoff((ConnectionError,))
    def create_index(self, index_name: str) -> None:
        settings = {
            'refresh_interval': '1s',
            'analysis': {
                'filter': {
                    'english_stop': {
                        'type': 'stop',
                        'stopwords': '_english_'
                    },
                    'english_stemmer': {
                        'type': 'stemmer',
                        'language': 'english'
                    },
                    'english_possessive_stemmer': {
                        'type': 'stemmer',
                        'language': 'possessive_english'
                    },
                    'russian_stop': {
                        'type': 'stop',
                        'stopwords': '_russian_'
                    },
                    'russian_stemmer': {
                        'type': 'stemmer',
                        'language': 'russian'
                    }
                },
                'analyzer': {
                    'ru_en': {
                        'tokenizer': 'standard',
                        'filter': [
                            'lowercase',
                            'english_stop',
                            'english_stemmer',
                            'english_possessive_stemmer',
                            'russian_stop',
                            'russian_stemmer'
                        ]
                    }
                }
            }
        }

        mappings = {
            'dynamic': 'strict',
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'imdb_rating': {
                    'type': 'float'
                },
                'genre': {
                    'type': 'keyword'
                },
                'title': {
                    'type': 'text',
                    'analyzer': 'ru_en',
                    'fields': {
                        'raw': {
                            'type': 'keyword'
                        }
                    }
                },
                'description': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                },
                'director': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                },
                'actors_names': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                },
                'writers_names': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                },
                'actors': {
                    'type': 'nested',
                    'dynamic': 'strict',
                    'properties': {
                        'id': {
                            'type': 'keyword'
                        },
                        'name': {
                            'type': 'text',
                            'analyzer': 'ru_en'
                        }
                    }
                },
                'writers': {
                    'type': 'nested',
                    'dynamic': 'strict',
                    'properties': {
                        'id': {
                            'type': 'keyword'
                        },
                        'name': {
                            'type': 'text',
                            'analyzer': 'ru_en'
                        }
                    }
                }
            },
        }

        with connection_to_els(self.database) as els:
            if not els.ping():
                raise elasticsearch.exceptions.ConnectionError
            if not els.indices.exists(index='movies'):
                els.indices.create(index=index_name, settings=settings, mappings=mappings)

    def load_filmworks(self, data: list[dict]) -> None:
        actions = [{'_index': 'movies', '_id': row['id'], '_source': row, } for row in data]

        with connection_to_els(self.database) as els:
            helpers.bulk(els, actions)
            self.logger.info('Loading has completed.')
