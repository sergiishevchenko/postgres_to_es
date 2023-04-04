import abc
import json
import os

from typing import Any, Dict
from json import JSONDecodeError
from redis import Redis


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        pass


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл.

    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        with open(self.file_path, 'w+') as f:
            json.dump(state, f)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        result = {}
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r+') as f:
                try:
                    result = json.load(f)
                except JSONDecodeError:
                    pass
        else:
            print('File has not found')
        return result


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        data = self.storage.retrieve_state()
        data.update({key: value})
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        data = self.storage.retrieve_state()
        return data.get(key, None)


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis):
        self.redis_adapter = redis_adapter

    def save_state(self, state: Dict[str, Any]) -> None:
        self.redis_adapter.set('data', json.dumps(state))

    def retrieve_state(self) -> Dict[str, Any]:
        data = self.redis_adapter.get('data')
        if data:
            return json.loads(data)
        return dict()