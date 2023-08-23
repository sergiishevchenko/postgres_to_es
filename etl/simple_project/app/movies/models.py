from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import UUIDMixin, TimeStampedMixin


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('actor')
    WRITER = 'writer', _('writer')
    DIRECTOR = 'director', _('director')


class FilmType(models.TextChoices):
    movie = 'movie', _('movie')
    tv_show = 'tv_show', _('tv_show')


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = 'content\'.\'genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.TextField(_('type'), choices=FilmType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')

    class Meta:
        db_table = 'content\'.\'film_work'
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\'.\'genre_film_work'
        indexes = [models.Index(fields=['film_work_id', 'genre_id'], name='film_work_genre')]
        verbose_name = _('Жанр фильма')
        verbose_name_plural = _('Жанры фильма')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = 'content\'.\'person'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\'.\'person_film_work'
        indexes = [models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role',)]
        verbose_name = _('Сотрудник кинопроизведения')
        verbose_name_plural = _('Сотрудники кинопроизведения')