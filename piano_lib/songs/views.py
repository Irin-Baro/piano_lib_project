from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import FileResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

from .models import (Author, Song, Category,
                     Comment, Like, SongCountViews)
from .forms import CommentForm


def paginator(queryset, page_number):
    paginator = Paginator(queryset, settings.SONGS_PER_PAGE)
    return paginator.get_page(page_number)


def index(request):
    """Главная страница"""
    page_obj = paginator(
        Song.objects.select_related('author', 'category'),
        request.GET.get('page')
    )
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'songs/index.html', context)


def category_list(request, slug):
    """Страница категории"""
    category = get_object_or_404(Category, slug=slug)
    page_obj = paginator(
        category.songs.select_related('author'), request.GET.get('page')
    )
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'songs/category_list.html', context)


def profile(request, author_id):
    """Страница автора"""
    author = get_object_or_404(Author, id=author_id)
    page_obj = paginator(
        author.songs.select_related('category'), request.GET.get('page')
    )
    context = {
        'author': author,
        'page_obj': page_obj
    }
    return render(request, 'songs/profile.html', context)


def song_detail(request, song_id):
    """Страница песни"""
    song = get_object_or_404(
        Song.objects.select_related('author', 'category'), pk=song_id)
    comments = song.comments.select_related('author')
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    is_views = SongCountViews.objects.filter(songId=song.id, sesId=session_key)
    if is_views.count() == 0 and str(session_key) != 'None':
        views = SongCountViews()
        views.sesId = session_key
        views.songId = song
        views.save()
        song.count_views += 1
        song.save()
    context = {
        'song': song,
        'comments': comments,
        'form': CommentForm(),
    }
    return render(request, 'songs/song_detail.html', context)


def song_download(request, song_id):
    """Функция загрузки песни"""
    song = get_object_or_404(
        Song.objects.select_related('author', 'category'), pk=song_id)
    song_file_path = song.song_file.path
    response = FileResponse(open(song_file_path, 'rb'),
                            content_type='application/pdf')
    response['Content-Disposition'] = ('inline; filename='
                                       f'"{song.song_title}.pdf"')
    return response


@login_required
def add_comment(request, song_id):
    """Страница добавления комментария"""
    song = get_object_or_404(
        Song.objects.select_related('author', 'category'), pk=song_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.song = song
        comment.save()
    return redirect('songs:song_detail', song_id=song_id)


@login_required
def comment_edit(request, comment_id):
    """Страница для редактирования комментария"""
    comment = get_object_or_404(
        Comment.objects.select_related('author'), pk=comment_id
    )
    if comment.author == request.user:
        form = CommentForm(request.POST or None,
                           instance=comment)
        if form.is_valid():
            form.save()
            return redirect('songs:song_detail', comment.song.pk)
        return render(request,
                      'songs/includes/comment_edit.html',
                      {'form': form})
    return redirect('songs:song_detail', song_id=comment.song.pk)


@login_required
def delete_comment(request, comment_id):
    """Страница для удаления комментария"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('songs:song_detail', song_id=comment.song.pk)


@login_required
def like_toggle(request, content_type_id, object_id):
    """Функция добавления/удаления лайков."""
    content_type = ContentType.objects.get_for_id(content_type_id)
    obj = get_object_or_404(content_type.model_class(), id=object_id)
    like, created = Like.objects.get_or_create(
        content_type=content_type,
        object_id=obj.id,
        user=request.user)
    if not created:
        was_liked = like.liked
        like.liked = not like.liked
        if was_liked:
            obj.likes.remove(like)
        else:
            obj.likes.add(like)
        like.save()
        obj.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def favorites_index(request):
    """Страница избранных песен"""
    page_obj = paginator(
        Song.objects.filter(likes__user=request.user, likes__liked=True),
        request.GET.get('page')
    )
    return render(request, 'songs/favorites.html', {'page_obj': page_obj})


class AllCategoryView(TemplateView):
    """Страница всех категорий."""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        context['category_all_url'] = reverse_lazy('songs:category_all')
        return context


class AllSongsView(TemplateView):
    """Страница всех песен."""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['songs'] = Song.objects.select_related('author', 'category')
        context['songs_all_url'] = reverse_lazy('songs:songs_all')
        return context


class AllAuthorsView(TemplateView):
    """Страница всех авторов."""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['authors'] = Author.objects.all()
        context['authors_all_url'] = reverse_lazy('songs:authors_all')
        return context
#
#
# @login_required
# def is_fan(obj, user) -> bool:
#     """Проверяет, лайкнул ли `user` `obj`.
#     """
#     if not user.is_authenticated:
#         return False
#     obj_type = ContentType.objects.get_for_model(obj)
#     likes = Like.objects.filter(
#         content_type=obj_type, object_id=obj.id, user=user)
#     return likes.exists()
#
#
# @login_required
# def get_fans(obj):
#     """Получает всех пользователей, которые лайкнули `obj`.
#     """
#     obj_type = ContentType.objects.get_for_model(obj)
#     return User.objects.filter(
#        likes__content_type=obj_type, likes__object_id=obj.id)
