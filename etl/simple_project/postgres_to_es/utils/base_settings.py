import dotenv

from pydantic import BaseModel, BaseSettings, Field


dotenv.load_dotenv()


class DataBase(BaseSettings):
    db_name: str = Field(..., env='DB_NAME')
    user: str = Field('app', env='DB_USER')
    password: str = Field(..., env='DB_PASSWORD')
    host: str = Field('127.0.0.1', env='DB_HOST')
    port: str = Field(5432, env='DB_PORT')


class ELSDefaultUrl(BaseSettings):
    els_host: str = Field(..., env='ELS_HOST')
    els_port: str = Field(9200, env='ELS_PORT')

    def get_url(self):
        return 'http://{}:{}'.format(self.es_host, self.es_port)


class BaseConfig(BaseSettings):
    page_size: int = Field(50, env='PAGE_SIZE')
    els_default_url: str = ELSDefaultUrl().get_url()
    database: dict = DataBase().dict()
    sleep_time: float = Field(60.0, env='ELS_SLEEP')


class ESPerson(BaseModel):
    id: str
    name: str


class ESFilmWork(BaseModel):
    id: str
    imdb_rating: float | None
    genre: list[str]
    title: str
    description: str | None
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[ESPerson]
    writers: list[ESPerson]