from django.urls import path

from . import views

app_name = 'songs'


urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites_index, name='favorites_index'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('profile/<int:author_id>/', views.profile, name='profile'),
    path('songs/<int:song_id>/', views.song_detail, name='song_detail'),
    path(
        'songs/<int:song_id>/comment/', views.add_comment,
        name='add_comment'
    ),
    path(
        'songs/comments/<int:comment_id>/edit/',
        views.comment_edit,
        name='comment_edit'
    ),
    path(
        'songs/comments/<int:comment_id>/delete/',
        views.delete_comment,
        name='delete_comment'
    ),
    path(
        'songs/<int:content_type_id>/<int:object_id>/like',
        views.like_toggle,
        name='like_toggle'
    ),
    path('songs/<int:song_id>/download/',
         views.song_download,
         name='song_download'),
]
