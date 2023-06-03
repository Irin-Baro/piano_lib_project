from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категории"""
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
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_title


class Author(models.Model):
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
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.author_name


class Song(models.Model):
    """Модель песни"""
    NUMBER_OF_CHAR: int = 15

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
        help_text='Укажите имя автора песни'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='songs',
        verbose_name='Категория',
        help_text='Укажите название категории'
    )
    song_file = models.FileField(
        verbose_name='Файл песни',
        help_text='Загрузите файл песни',
        upload_to='songs/',
        blank=True
    )
    count_views = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров песни'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'

    def __str__(self):
        return self.song_title


class Comment(models.Model):
    """Модель комментария"""
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

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liker',
        verbose_name='Лайкер'
    )
    post = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='like'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Нравится'
        verbose_name_plural = 'Нравятся'


class SongCountViews(models.Model):
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
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Количество просмотров'
