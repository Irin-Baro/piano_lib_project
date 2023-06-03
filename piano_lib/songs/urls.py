from django.urls import path

from . import views

app_name = 'songs'


urlpatterns = [
    path('', views.index, name='index'),
    # path('songs/', views.songs, name='song_list'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('profile/<int:author_id>/', views.profile, name='profile'),
    path('songs/<int:song_id>', views.song_detail, name='song_detail'),
    path(
        'songs/<int:songs_id>/comment/', views.add_comment,
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
        'songs/<str:username>/<int:song_id>/like/',
        views.song_like,
        name='song_like'
    ),
    path(
        'songs/<str:username>/<int:song_id>/dislike/',
        views.song_dislike,
        name='song_dislike'
    ),
]
