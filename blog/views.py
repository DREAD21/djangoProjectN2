from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm, CommentForm
from .models import Post

# Create your views here.
def post_list(request):
   posts = Post.objects.for_user(user=request.user)
   return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.is_published() and not request.user.is_staff:
        raise Http404("Запись в блоге не найдена")
    return render(request, 'blog/post_detail.html', {'post': post})

def error_404_view(request, exception):
    return render(request, '404.html')

@login_required
def post_edit(request, id=None):
   if request.user.is_authenticated:
       return post_update(request, id)
   return redirect('post_list')

def post_update(request, id):
    post = get_object_or_404(Post, id=id) if id else None

    if post and post.author != request.user:
        return redirect('post_list')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.is_published:
                post.published_date = timezone.now()
            else:
                post.published_date = None
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required()
def post_publish(request, id):
    post = get_object_or_404(Post, id=id)
    post.publish()
    return redirect('post_detail', id=id)

def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm(instance=post)
    return render(request, 'blog/add_comment.html', {'form': form})
