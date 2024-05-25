from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

MAX_LENGTH = 256
User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name=_('Опубликовано'),
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name=_('Заголовок'),
        help_text=_('Введите заголовок категории')
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        help_text=_('Введите описание категории')
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=_('Идентификатор'),
        help_text=_('Идентификатор страницы для URL; '
                    'разрешены символы латиницы, цифры, '
                    'дефис и подчёркивание.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Добавлено')
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')


class Location(PublishedModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name=_('Название места'),
        help_text=_('Введите название места')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Добавлено')
    )

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')


class Post(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name=_('Заголовок'),
        help_text=_('Введите заголовок публикации')
    )
    text = models.TextField(
        verbose_name=_('Текст'),
        help_text=_('Введите текст публикации')
    )
    pub_date = models.DateTimeField(
        verbose_name=_('Дата и время публикации'),
        help_text=_('Если установить дату и время в будущем — '
                    'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Автор публикации'),
        help_text=_('Выберите автора публикации')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Местоположение'),
        help_text=_('Выберите местоположение публикации')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Категория'),
        related_name='posts',  # Устанавливаем имя обратной связи
        help_text=_('Выберите категорию публикации')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Добавлено')
    )

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        default_related_name = 'posts'
        ordering = ['-pub_date']
