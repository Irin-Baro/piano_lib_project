from django.contrib import admin
from .models import Author, Category, Comment, File, Song, Video


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title', 'slug', 'description')
    search_fields = ('category_title',)
    list_filter = ('category_title',)
    empty_value_display = '-пусто-'


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_title', 'file', 'difficulty')
    list_editable = ('difficulty',)
    search_fields = ('file_title',)
    empty_value_display = '-пусто-'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('video_title', 'link', 'difficulty')
    list_editable = ('difficulty',)
    # search_fields = ('video_title',)
    empty_value_display = '-пусто-'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'song_title',
        'author',
        'display_files',
        'display_videos',
        'display_categories',
        'description',
        'image',
        'pub_date',
    )
    filter_horizontal = ('categories', 'files', 'videos')
    list_editable = ('author', 'song_title', 'description', 'image',)
    # search_fields = ('song_title', 'author__author_name', 'pub_date')
    list_filter = ('song_title', 'pub_date', 'author', 'categories')
    empty_value_display = '-пусто-'

    def display_categories(self, obj):
        return ', '.join([category.category_title for category
                          in obj.categories.all()])
    display_categories.short_description = 'Категории'

    def display_files(self, obj):
        return ', '.join([file.file_title for file
                          in obj.files.all()])
    display_files.short_description = 'Файлы'

    def display_videos(self, obj):
        return ', '.join([video.video_title for video
                          in obj.videos.all()])
    display_videos.short_description = 'Видео'


@admin.register(Author)
class Author(admin.ModelAdmin):
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
