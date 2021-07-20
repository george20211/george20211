from django.core import paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Group, Post, User, Comment
from django.views.decorators.cache import cache_page

@cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "index.html", {'page': page, })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "group.html", {"group": group,
                  'page': page})


class JustStaticPage(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['just_title'] = 'Очень простая страница'
        context['just_text'] = 'я молодец'
        return context


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    author_posts = profile.posts.all()
    paginator = Paginator(author_posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "profile": profile,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    comments = post.comments.all()
    paginator = Paginator(comments, 15)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    form = CommentForm(request.POST or None)
    context = {
        "author_posts": post.author,
        "post": post,
        'form': form,
        'comments': comments,
        'page': page,
    }
    return render(request, 'post.html', context)


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'new.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.user != post.author:
        return redirect('post', username, post_id)
    if form.is_valid():
        post.save()
        return redirect('post', username, post_id)
    return render(request, 'new.html', {'form': form, 'post': post})


def stats(request):
    post_count_all = len(Post.objects.all())
    users_count_all = len(User.objects.all())
    last_register = User.date_joined
    context = {
        'post_count_all': post_count_all,
        'users_count_all': users_count_all,
        'last_register': last_register,
    }
    return render(request, 'top.html', context)

def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    comments = post.comments.all()
    author = request.user
    form = CommentForm(request.POST or None)
    context = {
        'post': post,
        'author_posts': post.author,
        'form': form,
        'author': author,
        'comments': comments,
    }
    if form.is_valid():
        comments = form.save(commit=False)
        comments.author = request.user
        comments.post = post
        comments.save()
        return render(request, 'comments.html', context)
        #return redirect('post', username=username, post_id=post_id)
    return render(request, 'comments.html', context)

def page_not_found(request, exception):

    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
