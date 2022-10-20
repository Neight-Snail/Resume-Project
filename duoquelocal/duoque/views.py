from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CustomUserCreationForm, PostCreationForm
from django.contrib.auth import login,logout
from django.contrib import messages
from duoque.models import Post
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from django.db import connection



def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, "duoque/homepage.html", {"user": request.user, "posts": posts})
    else:
        return redirect("accounts/login")

def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('index')
    else:
        f = CustomUserCreationForm()
    return render(request, 'duoque/register.html', {'form': f})

def create_post(request):
    if request.method == 'POST':
        f = PostCreationForm(request.POST, request.FILES)
        if f.is_valid():
            p = Post()
            p.clip = f.cleaned_data['post']
            p.author = request.user
            p.pub_date = datetime.date.today()
            p.save()
            p.likes.add(request.user)
            messages.success(request, "Post made successfully")
            return redirect('index')
    else:
        f=PostCreationForm()
    return render(request, 'duoque/create_post.html', {'form': f})

def upvote(request,post_id):
    p = Post.objects.get(pk=post_id)
    p.likes.add(request.user)
    return HttpResponseRedirect(reverse('index'))

def downvote(request,post_id):
    p = Post.objects.get(pk=post_id)
    p.likes.remove(request.user)
    return HttpResponseRedirect(reverse('index'))

def edit_post(request,post_id):
    try:
        p = Post.objects.get(pk=post_id, author=request.user)
    except Post.DoesNotExist:
        p = None

    if request.method == 'POST':
        f = PostCreationForm(request.POST, request.FILES)
        if p and f.is_valid():
            p.clip = f.cleaned_data['post']
            p.save()            
            messages.success(request, "Post edited successfully")
            return redirect('index')

    elif p:
        f=PostCreationForm(initial={'clip': p.clip})
    else:
        return redirect('index')
    return render(request, 'duoque/create_post.html', {'form': f, 'post_to_be_edited': p})

def view_profile(request,username):
    if not request.user.is_authenticated:
        return redirect("accounts/login")
    u = get_object_or_404(User, username__iexact=username)
    posts = Post.objects.filter(author = u)
    return render(request, "duoque/profile.html", {"user": u, "posts": posts, "logged_in_user": request.user})

def delete_post(request,post_id):
    try:
        p = Post.objects.get(pk=post_id, author=request.user)
    except Post.DoesNotExist:
        p = None

    if p:
        p.delete()
        return redirect("index")

def stats(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT duoque_post.clip, auth_user.username FROM duoque_post LEFT JOIN auth_user ON duoque_post.author_id = auth_user.id''')
    rows = cursor.fetchall()
    return render(request, "duoque/stats.html", {'rows': rows})

def logout_user(request):
    logout(request)