from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CustomUserCreationForm
from .models import User, Post
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q, Count

# View for the main page. Displays all posts and handles the creation of new posts.
@login_required
def index(request):
    # Handle new post creation
    if request.method == "POST" and request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
    
    # Fetch and paginate posts
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if the user liked each post
    for post in page_obj:
        post.is_liked_by_user = request.user in post.likes.all()

    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": page_obj,
    })

# View to handle user login.
def login_view(request):
    if request.method == "POST":
        # Authenticate the user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

# View to log out the current user.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# View to handle user registration.
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            confirmation = form.cleaned_data.get("confirmation")
            if password != confirmation:
                return render(request, "network/register.html", {
                    "form": form,
                    "message": "Passwords must match."
                })
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
        return render(request, "network/register.html", {"form": form})

# View for user profile pages. Shows posts and handles follow/unfollow actions.
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all().order_by('-created_at')
    is_following = request.user.is_authenticated and profile_user.followers.filter(id=request.user.id).exists()

    # Check if the user liked each post
    if request.user.is_authenticated:
        for post in posts:
            post.is_liked_by_user = post.likes.filter(id=request.user.id).exists()

    # Handle follow/unfollow actions
    if request.method == "POST" and request.user.is_authenticated:
        if request.user != profile_user:
            if is_following:
                profile_user.followers.remove(request.user)
            else:
                profile_user.followers.add(request.user)
            return redirect('profile', username=username)

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
    })

# View to display posts from users the current user is following.
@login_required
def following_view(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')

    # Check if the user liked each post
    for post in posts:
        post.is_liked_by_user = post.likes.filter(id=request.user.id).exists()
        
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": page_obj,
    })

# View to edit an existing post.
@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found or unauthorized."}, status=404)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        new_content = data.get("content", "")
        if new_content.strip():
            post.content = new_content
            post.save()
            return JsonResponse({"message": "Post updated successfully."}, status=200)
        else:
            return JsonResponse({"error": "Content cannot be empty."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=400)

# View to like or unlike a post.
@login_required
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "POST":
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            "liked": liked,
            "like_count": post.like_count()
        }, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=400)

# View to search for posts and users.
@login_required
def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(Q(content__icontains=query))
    users = User.objects.filter(Q(username__icontains=query))

    return render(request, "network/search.html", {
        "query": query,
        "posts": posts,
        "users": users,
    })
