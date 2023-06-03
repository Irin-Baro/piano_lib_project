from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Author, Song, Category, Comment, Like, SongCountViews
from .forms import CommentForm


def paginator(queryset, page_number):
    paginator = Paginator(queryset, settings.SONGS_PER_PAGE)
    return paginator.get_page(page_number)


def index(request):
    """Главная страница"""
    songs = Song.objects.all()
    context = {
        'songs': songs,
    }
    return render(request, 'songs/index.html', context)


def category_list(request, slug):
    """Страница категории"""
    category = get_object_or_404(Category, slug=slug)
    songs = Song.objects.filter(category=category)
    context = {
        'category': category,
        'songs': songs
    }
    return render(request, 'songs/category_list.html', context)


def profile(request, author_id):
    """Страница автора"""
    author = get_object_or_404(Author, id=author_id)
    songs = Song.objects.filter(author=author_id)
    context = {
        'author': author,
        'songs': songs
    }
    return render(request, 'songs/profile.html', context)


def song_detail(request, song_id):
    """Страница записи"""
    song = get_object_or_404(
        Song.objects.select_related('author', 'category'), pk=song_id)
    comments = song.comments.select_related('author')
    # author = get_object_or_404(User, username=song.author.username)
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    is_views = SongCountViews.objects.filter(songId=song.id, sesId=session_key)
    if is_views.count() == 0 and str(session_key) != 'None':
        views = SongCountViews()
        views.sesId = session_key
        views.postId = song
        views.save()
        song.count_views += 1
        song.save()
    is_liked = (
        request.user.is_authenticated
        and song.like.filter(user_id=request.user))
    context = {
        'song': song,
        'comments': comments,
        'form': CommentForm(),
        'is_liked': is_liked,
    }
    return render(request, 'songs/song_detail.html', context)



@login_required
def add_comment(request, song_id):
    """Страница добавления комментария"""
    song = get_object_or_404(
        Song.objects.select_related('author', 'group'), pk=song_id)
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
    return redirect('songs:song_detail', post_id=comment.song.pk)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('songs:song_detail', song_id=comment.song.pk)


@login_required
def song_like(request, username, song_id):
    song = get_object_or_404(Song, author__username=username, pk=song_id)
    Like.objects.get_or_create(user=request.user, song=song)
    return redirect('songs:song_detail', song_id=song_id)


@login_required
def song_dislike(request, username, song_id):
    song = get_object_or_404(Song, author__username=username, pk=song_id)
    Like.objects.filter(user=request.user, song=song).delete()
    return redirect('songs:song_detail', post_id=song_id)
