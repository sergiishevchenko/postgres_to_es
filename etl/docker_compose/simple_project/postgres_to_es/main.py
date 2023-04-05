import datetime
import logging
import time

import elasticsearch
import psycopg2

from etl_modules.extractor import PostgresExtractor
from etl_modules.loader import ElasticsearchLoader
from etl_modules.transformer import DataTransform
from sqlite_to_postgres.logger import get_logger
from state_config import State, JsonFileStorage
from utils.backoff import backoff
from utils.base_settings import BaseConfig


@backoff((psycopg2.OperationalError,))
@backoff((elasticsearch.exceptions.ConnectionError,))
def extract_transform_load(logger: logging.Logger, extractor: PostgresExtractor, transformer: DataTransform, state: State, loader: ElasticsearchLoader) -> None:
    last_timestamp = state.get_state('last_timestamp')
    start_timestamp = datetime.datetime.now()
    filmworks = state.get_state('filmworks')

    for extracted_filmworks in extractor.extract_filmworks(last_timestamp, start_timestamp, filmworks):
        transformed_filmworks = transformer.transform_filmworks(extracted_filmworks)
        loader.load_filmworks(transformed_filmworks)
        state.set_state('last_timestamp', str(start_timestamp))
        state.set_state('filmworks', [])


if __name__ == '__main__':
    logger = get_logger(__name__)
    base_config = BaseConfig()

    storage_state = State(
        JsonFileStorage(file_path='state_storage.json')
    )
    extractor = PostgresExtractor(
        psql=base_config.database,
        page_size=base_config.page_size,
        storage_state=storage_state,
        logger=logger
    )
    transformer = DataTransform()
    loader = ElasticsearchLoader(
        database=base_config.els_default_url,
        logger=logger
    )

    while True:
        extract_transform_load(logger, extractor, transformer, storage_state, loader)
        logger.info('extract_transform_load method has started...')
        time.sleep(base_config.sleep_time)
