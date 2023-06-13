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
    path(
        'category/',
        views.AllCategoryView.as_view(template_name='songs/category_all.html'),
        name='category_all'),
    path(
        'songs/',
        views.AllSongsView.as_view(template_name='songs/songs_all.html'),
        name='songs_all'),
    path(
        'authors/',
        views.AllAuthorsView.as_view(template_name='songs/authors_all.html'),
        name='authors_all'),
]
