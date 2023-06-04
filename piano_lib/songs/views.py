from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import FileResponse

from .models import (Author, Song, Category,
                     Comment, Like)
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
    is_liked = (
        request.user.is_authenticated
        and song.like.filter(user_id=request.user))
    context = {
        'song': song,
        'comments': comments,
        'form': CommentForm(),
        'is_liked': is_liked,
    }
    if 'song_id' not in request.COOKIES:
        response = render(request, 'songs/song_detail.html', context)
        response.set_cookie('song_id', song.id, max_age=60*60*24)
        song.count_views += 1
        song.save()
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
def song_like(request, username, song_id):
    """Функция добавления песни в избранное"""
    song = get_object_or_404(Song, author__author_name=username, pk=song_id)
    Like.objects.get_or_create(user=request.user, song=song)
    return redirect('songs:song_detail', song_id=song_id)


@login_required
def song_dislike(request, username, song_id):
    """Функция удаления песни из избранных"""
    song = get_object_or_404(Song, author__author_name=username, pk=song_id)
    Like.objects.filter(user=request.user, song=song).delete()
    return redirect('songs:song_detail', song_id=song_id)


@login_required
def favorites_index(request):
    """Страница избранных песен"""
    page_obj = paginator(
        Song.objects.select_related('author', 'category')
        .filter(like__user_id=request.user),
        request.GET.get('page')
    )
    return render(request, 'songs/favorites.html', {'page_obj': page_obj})
