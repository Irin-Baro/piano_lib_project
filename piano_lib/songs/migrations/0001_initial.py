# Generated by Django 2.2.19 on 2023-06-03 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(help_text='Укажите автора', max_length=200, verbose_name='Автор')),
                ('description', models.TextField(blank=True, help_text='Укажите информацию оь авторе', verbose_name='Об авторе')),
                ('image', models.ImageField(blank=True, help_text='Загрузите изображение', null=True, upload_to='pictures/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(help_text='Укажите название категории', max_length=200, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Укажите уникальный фрагмент URL-адреса категории', unique=True, verbose_name='Уникальный фрагмент URL-адреса категории')),
                ('description', models.TextField(help_text='Здесь должно быть описание категории', verbose_name='Описание категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_title', models.CharField(help_text='Укажите название песни', max_length=200, verbose_name='Название песни')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('song_file', models.FileField(blank=True, help_text='Загрузите файл песни', upload_to='songs/', verbose_name='Файл песни')),
                ('count_views', models.PositiveIntegerField(default=0, verbose_name='Количество просмотров песни')),
                ('author', models.ForeignKey(help_text='Укажите имя автора песни', on_delete=django.db.models.deletion.CASCADE, related_name='songs', to=settings.AUTH_USER_MODEL, verbose_name='Автор песни')),
                ('category', models.ForeignKey(blank=True, help_text='Укажите название категории', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='songs', to='songs.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Песня',
                'verbose_name_plural': 'Песни',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='SongCountViews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sesId', models.CharField(db_index=True, max_length=150)),
                ('songId', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='songs.Song')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='songs.Song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to=settings.AUTH_USER_MODEL, verbose_name='Лайкер')),
            ],
            options={
                'verbose_name': 'Нравится',
                'verbose_name_plural': 'Нравятся',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Разместите здесь комментарий', verbose_name='Текст комментария')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания комментария')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='songs.Song', verbose_name='песня')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-created',),
            },
        ),
    ]