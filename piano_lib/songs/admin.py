from django.contrib import admin
from .models import Author, Song, Category, Comment, Like, SongCountViews


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'song_title',
        'author',
        'category',
        'pub_date',
        'song_file',

    )
    list_editable = ('author', 'category', 'song_file', 'song_title')
    search_fields = ('song_title', 'category', 'author', 'pub_date')
    list_filter = ('pub_date', 'category', 'author',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('category_title', 'slug', 'description')
    search_fields = ('category_title',)
    list_filter = ('category_title',)
    empty_value_display = '-пусто-'


@admin.register(Author)
class Author(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'image', 'description')
    list_editable = ('image', 'description')
    search_fields = ('author_name',)
    list_filter = ('author_name',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('song', 'author', 'text', 'created')
    list_filter = ('author', 'created')


admin.site.register(Like)
admin.site.register(SongCountViews)
