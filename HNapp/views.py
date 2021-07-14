from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import datetime
from .forms import *
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .scraping import scrap
from django.contrib.auth.models import User


def comment_reply_view(request, id1, id2):
    form = CommentForm()
    comment = Comment.objects.get(id=id2)
    post = Post.objects.get(id=id1)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                reply_comment_content = form.cleaned_data['content']
                identifier = int(comment.identifier + 1)
                reply_comment = Comment(creator=request.user, post=post, content=reply_comment_content, parent=comment,
                                        identifier=identifier)
                reply_comment.save()
                return redirect(f'/post/{id1}')
        return redirect('/signin')
    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'HNapp/reply_post.html', context)


def comment_list_view(request, id):
    form = CommentForm()
    post = Post.objects.get(id=id)
    post.count_votes()
    post.count_comments()
    comments = []

    def func(i, parent):
        children = Comment.objects.filter(post=post).filter(identifier=i).filter(parent=parent)
        for child in children:
            gchildren = Comment.objects.filter(post=post).filter(identifier=i + 1).filter(parent=child)
            if len(gchildren) == 0:
                comments.append(child)
            else:
                func(i + 1, child)
                comments.append(child)
    func(0, None)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                comment = Comment(creator=request.user, post=post, content=content, identifier=0)
                comment.save()
                return redirect(f'/post/{id}')
        return redirect('/signin')
    context = {
        'form': form,
        'post': post,
        'comments': list(reversed(comments)),
    }
    return render(request, 'HNapp/comment_post.html', context)


def up_vote_view(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        votes = Vote.objects.filter(post=post)
        v = votes.filter(voter=request.user)
        if len(v) == 0:
            upvote = Vote(voter=request.user, post=post)
            upvote.save()
            return redirect('/')
    return redirect('/signin')


def down_vote_view(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        votes = Vote.objects.filter(post=post)
        v = votes.filter(voter=request.user)
        if len(v) != 0:
            v.delete()
            return redirect('/')
    return redirect('/signin')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'HNapp/auth_signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'HNapp/auth_signup.html', {'form': form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm()
            return render(request, 'HNapp/auth_signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'HNapp/auth_signin.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('/')


def submit_post_view(request):
    if request.user.is_authenticated:
        form = PostForm()
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                url = form.cleaned_data['url']
                creator = request.user
                created_on = datetime.now()
                post = Post(title=title, url=url, creator=creator, created_on=created_on)
                post.save()
                return redirect('/')
        return render(request, 'HNapp/submit.html', {'form': form})
    return redirect('/signin')


def edit_post_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = PostForm(instance=post)
    return render(request, 'HNapp/submit.html', {'form': form})


def post_list_view(request):
    posts = Post.objects.all()
    for post in posts:
        post.count_votes()
        post.count_comments()
    context = {
        'posts': posts,
    }
    return render(request, 'HNapp/postlist.html', context)


def new_post_list_view(request):
    posts = Post.objects.all().order_by('-created_on')
    for post in posts:
        post.count_votes()
        post.count_comments()
    context = {
        'posts': posts,
    }
    return render(request, 'HNapp/postlist.html', context)


def user_info_view(request, username):
    user = User.objects.get(username=username)
    context = {'user': user}
    return render(request, 'HNapp/user_info.html', context)


def user_submissions(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(creator=user)
    for post in posts:
        post.count_votes()
        post.count_comments()
    context = {
        'posts': posts,
    }
    return render(request, 'HNapp/user_posts.html', context)


def parse_site(request):
    p = Post.objects.all()
    p.delete()
    scrap()
    return redirect('/')


def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('/')


