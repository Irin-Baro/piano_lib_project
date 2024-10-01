from django.contrib import admin
from .models import (Author, Category, Comment,
                     Song, SongFile)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title', 'slug', 'description')
    search_fields = ('category_title',)
    list_filter = ('category_title',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('category_title',)}


@admin.register(SongFile)
class SongFileAdmin(admin.ModelAdmin):
    list_display = ('display_song_title', 'file', 'difficulty', 'video')
    list_editable = ('difficulty',)
    search_fields = ('display_song_title',)
    empty_value_display = '-пусто-'

    def display_song_title(self, obj):
        return obj.song.song_title
    display_song_title.short_description = 'Название песни'


class SongFileInline(admin.TabularInline):
    model = SongFile
    extra = 0


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """Отображение модели Song."""
    inlines = [SongFileInline]
    list_display = (
        'song_title',
        'pk',
        'get_files',
        'display_categories',
        'author',
        # 'display_files',
        'description',
        'image',
        'pub_date',
    )
    filter_horizontal = ('categories',)
    list_editable = ('description', 'image',)
    search_fields = ('song_title', 'author__author_name')
    list_filter = ('song_title', 'pub_date', 'author', 'categories')
    empty_value_display = '-пусто-'

    def display_categories(self, obj):
        return ', '.join([category.category_title for category
                          in obj.categories.all()])
    display_categories.short_description = 'Категории'

    def get_files(self, obj):
        return ', '.join([file_obj.difficulty for file_obj
                          in obj.songfiles.all()])
    get_files.short_description = 'Файлы и их сложность'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Отображение модели Author."""
    list_display = ('id', 'author_name', 'image', 'description')
    list_editable = ('author_name', 'image', 'description')
    # search_fields = ('author_name',)
    list_filter = ('author_name',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('song', 'author', 'text', 'created')
    list_filter = ('author', 'created')


# admin.site.register(Like)
# admin.site.register(SongCountViews)
