import dotenv

from pydantic import (BaseSettings, Field)


dotenv.load_dotenv()


class DataBase(BaseSettings):
    db_name: str = Field(..., env='DB_NAME')
    user: str = Field('app', env='DB_USER')
    password: str = Field(..., env='DB_PASSWORD')
    host: str = Field('127.0.0.1', env='DB_HOST')
    port: str = Field(5432, env='DB_PORT')


class ESDefaultUrl(BaseSettings):
    es_host: str = Field(..., env='ES_HOST')
    es_port: str = Field(9200, env='ES_PORT')

    def get_url(self):
        return 'http://{}:{}'.format(self.es_host, self.es_port)


class BaseConfig(BaseSettings):
    page_size: int = Field(50, env='PAGE_SIZE')
    es_default_url: str = ESDefaultUrl().get_url()
    database: dict = DataBase().dict()
    sleep_time: float = Field(60.0, env='ETL_SLEEP')
