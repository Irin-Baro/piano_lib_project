from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (GenericRelation,
                                                GenericForeignKey)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

User = get_user_model()


CHOICES = (
    ('easy', 'легкая версия'),
    ('medium', 'удобное переложение'),
    ('hard', 'для опытных музыкантов')
)


class Category(models.Model):
    """Модель категории."""
    category_title = models.CharField(
        max_length=200,
        verbose_name='Название категории',
        help_text='Укажите название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный фрагмент URL-адреса категории',
        help_text='Укажите уникальный фрагмент URL-адреса категории'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание категории',
        help_text='Здесь должно быть описание категории'
    )

    class Meta:
        ordering = ('category_title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_title


class Author(models.Model):
    """Модель автора песни."""
    author_name = models.CharField(
        max_length=200,
        verbose_name='Автор',
        help_text='Укажите автора'
        )
    description = models.TextField(
        blank=True,
        verbose_name='Об авторе',
        help_text='Укажите информацию об авторе'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Загрузите изображение',
        upload_to='pictures/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('author_name',)
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.author_name


class Like(models.Model):
    """Модель лайка для песни."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Лайкер'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True
    )
    object_id = models.PositiveIntegerField(
        null=True,
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    liked = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Video(models.Model):
    """Модель ссылки на видео."""
    video_title = models.CharField(
        max_length=200,
        verbose_name='Название видео',
        help_text='Укажите название видео'
    )
    link = models.URLField(
        verbose_name='Ссылка на видео',
        help_text='Укажите cсылку на видео'
    )
    difficulty = models.CharField(
        max_length=16,
        choices=CHOICES,
        null=True,
        blank=True,
        verbose_name='Сложность',
        help_text='Выберите сложность'
    )

    class Meta:
        ordering = ('video_title',)
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.video_title


class File(models.Model):
    """Модель файла песни."""
    file_title = models.CharField(
        max_length=200,
        verbose_name='Название файла',
        help_text='Укажите название файла'
    )
    file = models.FileField(
        verbose_name='Файл песни',
        help_text='Загрузите файл песни',
        upload_to='songs/'
    )
    difficulty = models.CharField(
        max_length=16,
        choices=CHOICES,
        null=True,
        blank=True,
        verbose_name='Сложность',
        help_text='Выберите сложность'
    )

    class Meta:
        ordering = ('file_title',)
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.file_title


class Song(models.Model):
    """Модель песни."""
    song_title = models.CharField(
        max_length=200,
        verbose_name='Название песни',
        help_text='Укажите название песни'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='songs',
        verbose_name='Автор песни',
        help_text='Выберите имя автора песни'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='songs',
        verbose_name='Категории',
        help_text='Выберите категории песни',
        blank=True
    )
    files = models.ManyToManyField(
        File,
        verbose_name='Файлы',
        help_text='Выберите файлы песни',
        blank=True
    )
    videos = models.ManyToManyField(
        Video,
        verbose_name='Видео',
        help_text='Выберите видео',
        blank=True
    )
    description = models.TextField(
        blank=True,
        verbose_name='Информация о песни',
        help_text='Укажите информацию о песни'
    )
    count_views = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров песни'
    )
    likes = GenericRelation(Like)

    class Meta:
        ordering = ('song_title',)
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'

    def __str__(self):
        return self.song_title

    @property
    def get_likes_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(
            content_type=content_type,
            object_id=self.id,
            liked=True).count()

    @property
    def get_likes_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            'songs:like_toggle',
            kwargs={'content_type_id': content_type.id, 'object_id': self.id}
        )

    @property
    def get_users_who_liked(self):
        obj_type = ContentType.objects.get_for_model(self)
        likes = Like.objects.filter(content_type=obj_type, object_id=self.id)
        return [like.user for like in likes if like.liked]


class Comment(models.Model):
    """Модель комментария."""
    NUMBER_OF_CHAR: int = 15

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='песня'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Разместите здесь комментарий'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания комментария'
    )
    likes = GenericRelation(Like)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    @property
    def get_likes_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(
            content_type=content_type,
            object_id=self.id,
            liked=True).count()

    @property
    def get_likes_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            'songs:like_toggle',
            kwargs={'content_type_id': content_type.id, 'object_id': self.id}
        )

    @property
    def get_users_who_liked(self):
        obj_type = ContentType.objects.get_for_model(self)
        likes = Like.objects.filter(content_type=obj_type, object_id=self.id)
        return [like.user for like in likes if like.liked]


class SongCountViews(models.Model):
    """Модель счетчика просмотров."""
    # привязка к пользователю (сессии пользователя)
    sesId = models.CharField(
        max_length=150,
        db_index=True
    )
    # привязка к посту
    songId = models.ForeignKey(
        Song,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.sesId)
