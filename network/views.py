from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

import json

from .models import *


def index(request):
    return HttpResponseRedirect('/page/1')

def page(request, page):
    posts = Post.objects.all().order_by('-date')
    p = Paginator(posts, 10) # change to 10

    return render(request, "network/index.html", {
        "posts": p.page(page).object_list,
        "num_pages": p.num_pages,
        "pages": range(1, p.num_pages+1),
        "prev_page": page - 1,
        "next_page": page + 1,
        "active_page": page
    })

def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        post = Post(user=request.user, content=content)
        post.save()
    return HttpResponseRedirect(reverse("index"))

def follow(request, user):
    user_obj = User.objects.get(username=user)
    if user_obj not in request.user.following.all():
        # follow
        request.user.following.add(user_obj)
    else:
        # unfollow
        request.user.following.remove(user_obj)

    return HttpResponseRedirect(f'/profile/{user}/1')

def profile(request, name, page):
    if User.objects.filter(username=name).exists():
        user = User.objects.get(username=name)
        posts = user.posts.all().order_by('-date')
        p = Paginator(posts, 10)

        return render(request, "network/profile.html", {
            "username": name,
            "num_followers": user.followers.count(),
            "num_following": user.following.count(),
            "posts": p.page(page).object_list,
            "num_pages": p.num_pages,
            "pages": range(1, p.num_pages+1),
            "prev_page": page - 1,
            "next_page": page + 1,
            "active_page": page,
            "following": user in request.user.following.all()
        })

def following(request, page):
    posts = Post.objects.filter(user__in=request.user.following.all()).order_by('-date')
    p = Paginator(posts, 10) # change to 10

    return render(request, "network/following.html", {
        "posts": p.page(page).object_list,
        "num_pages": p.num_pages,
        "pages": range(1, p.num_pages+1),
        "prev_page": page - 1,
        "next_page": page + 1,
        "active_page": page
    })

@csrf_exempt
def edit(request, id):
    post = Post.objects.get(pk=id)
    if post.user == request.user:
        if request.method == "POST":
            body = json.loads(request.body)
            post.content = body["content"]
            post.save()

            return JsonResponse({
                "success": "Post saved successfully"
            })
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def update_like(request, id):
    post = Post.objects.get(pk=id)
    if request.user in post.liked_users.all():
        #unlike
        post.likes -= 1
        request.user.likes.remove(post)
        post.save()
        request.user.save()
        return JsonResponse({
            "liked": False
        })
    
    #like MIGRATE DB
    post.likes += 1
    request.user.likes.add(post)
    post.save()
    request.user.save()
    return JsonResponse({
        "liked": True
    })
    


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
