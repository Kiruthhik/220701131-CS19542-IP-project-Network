from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import  HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import *


def index(request):
    if request.method == "POST":
        content  = request.POST["content"]
        user = request.user
        post = Post.objects.create(content = content, posted_by = user)
        post.save()
    posts = Post.objects.all().order_by('-time')
    liked_post = []
    for post in posts:
        if request.user.liked.filter(id = post.id).exists():
            liked_post.append(post.id)
    paginator = Paginator(posts,10)
    page_no = request.GET.get('page',1)
    page_obj = paginator.get_page(page_no)
    context = {
        "posts":page_obj,
        "liked_posts":liked_post
    }
    return render(request, "network/index.html",context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def view_profile(request,username):
    user = get_object_or_404(User,username =username)
    followers_count = user.followers.count()
    following_count = user.following.count()
    posts = user.posts.all().order_by("-time")
    context = {
        "profile":user,
        "followers":followers_count,
        "following":following_count,
        "posts":posts
    }
    return render(request,"network/profile.html",context)

def follow(request,username):
    user = request.user
    following = get_object_or_404(User,username = username)
    if following in user.following.all():
        user.following.remove(following)
    else:
        user.following.add(following)
    return redirect(reverse('view_profile', args=[username]))

def following_page(request):
    user = request.user
    posts = Post.objects.filter(posted_by__in = user.following.all()).order_by("-time")
    liked_post = []
    for post in posts:
        if request.user.liked.filter(id = post.id).exists():
            liked_post.append(post.id)
    paginator = Paginator(posts,10)
    page_no = request.GET.get('page',1)
    page_obj = paginator.get_page(page_no)
    context = {
        "posts":page_obj,
        "liked_posts":liked_post
    }
    return render(request, "network/following.html",context)

def update_post(request,id):
    if request.method == "POST":
        post = get_object_or_404(Post,id=id)
        content = request.POST['updated_content']
        post.content = content
        post.save()
    return redirect(reverse('index'))

def likes(request,id):
    user = request.user
    post = Post.objects.get(id=id)
    if user.liked.filter(id=id).exists():
        post.liked_by.remove(user)
    else:
        post.liked_by.add(user)
    liked = user.liked.filter(id=id).exists()
    likes = post.liked_by.count()
    return JsonResponse({
        "liked":liked,
        "likes":likes
    })


