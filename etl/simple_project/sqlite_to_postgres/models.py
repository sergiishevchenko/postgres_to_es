from datetime import date, datetime
from enum import Enum
from typing import Optional
import uuid
from uuid import UUID

from dataclasses import dataclass, field, asdict


@dataclass
class UUIDMixin:
    '''UUIDMixin dataclass.'''

    id: UUID = field(default_factory=uuid.uuid4)


@dataclass
class CreateTimeMixin:
    '''TimeStampedMixin dataclass.'''

    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class UpdateTimeMixin:
    '''TimeStampedMixin dataclass.'''

    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Model:
    '''Model dataclass.'''

    @property
    def values(self):
        return '\t'.join([str(x) for x in asdict(self).values()])


@dataclass
class FilmType(str, Enum):
    '''FilmType dataclass.'''

    movie = 'movie'
    tv_show = 'tv_show'


@dataclass
class RoleType(str, Enum):
    '''RoleType dataclass.'''

    actor = 'actor'
    writer = 'writer'
    director = 'director'


@dataclass(order=True)
class FilmWork(Model, UUIDMixin, CreateTimeMixin, UpdateTimeMixin):
    '''FilmWork dataclass.'''

    title: str = None
    description: Optional[str] = None
    creation_date: Optional[date] = None
    file_path: Optional[str] = None
    rating: Optional[float] = None
    type: Optional[FilmType] = None


@dataclass(order=True)
class Person(Model, UUIDMixin, CreateTimeMixin, UpdateTimeMixin):
    '''Person dataclass.'''

    full_name: str = None


@dataclass(order=True)
class PersonFilmWork(Model, UUIDMixin, CreateTimeMixin):
    '''PersonFilmWork dataclass.'''

    person_id: UUID = field(default_factory=uuid.uuid4)
    film_work_id: UUID = field(default_factory=uuid.uuid4)
    role: Optional[RoleType] = None


@dataclass(order=True)
class Genre(Model, UUIDMixin, CreateTimeMixin, UpdateTimeMixin):
    '''Genre dataclass.'''

    name: str = None
    description: Optional[str] = None


@dataclass(order=True)
class GenreFilmWork(Model, UUIDMixin, CreateTimeMixin):
    '''GenreFilmWork dataclass.'''

    genre_id: UUID = field(default_factory=uuid.uuid4)
    film_work_id: UUID = field(default_factory=uuid.uuid4)
