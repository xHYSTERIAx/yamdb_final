from api.utils import gen_confirmation_code
from core.models import CreatedModel
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import correct_year

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'пользователь',),
    (MODERATOR, 'модератор',),
    (ADMIN, 'администратор',),
)


class User(AbstractUser):
    confirmation_code = models.CharField(
        max_length=10,
        verbose_name='Код подтверждения',
        default=gen_confirmation_code()
    )
    role = models.CharField(
        max_length=256,
        choices=ROLES,
        verbose_name='Роль'
    )
    bio = models.TextField(
        max_length=3500,
        blank=True,
        verbose_name='Информация о себе'
    )
    email = models.EmailField(
        max_length=250,
        unique=True,
        blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Жанр'
    )

    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название произведения'
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[correct_year]
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        null=True,
        on_delete=models.SET_NULL
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )

    def __str__(self):
        return self.name


class Review(CreatedModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Ваш отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Ваша оценка'
    )

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(
                fields=('title', 'author'), name='unique_title_author'
            )
        ]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Название произведения',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр : {self.genre}'


class Comments(CreatedModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(
        max_length=255,
        verbose_name='Ваш комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
