import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile


def index(request):
    return render(request, "network/index.html")


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

            # create a profile for user upon registration
            profile = Profile.objects.create(user=user)
            profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def new_post(request):

    # adding new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    # body: JSON.stringify({k: v})  <=== json.loads() to access body of request
    data = json.loads(request.body)
    content = data.get("content", "")

    try:
        user = User.objects.get(id=request.user.id)
        new_post = Post(user=user, content=content)
        new_post.save()

    # raise exception if user does not exist in database
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found!"}, status=404)

    result = {
        "message": "New post added successfully!",
        "user_id": request.user.id,
    }
    return JsonResponse(result, status=201)


def listing(request):
    post_list = Post.objects.all().order_by("-timestamp")

    # show 10 posts per page
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/list.html", {"page_obj": page_obj})


@login_required
def all_post(request):

    # return post objects in reverse chronological order
    post_objects = Post.objects.all().order_by("-timestamp")
    user = User.objects.get(id=request.user.id)

    posts = []
    for post in post_objects:

        posts.append({
            "id": post.id,
            "user_id": post.user.id,
            "username": post.user.username,
            "content": post.content,
            "likes": post.likes_num(),
            "timestamp": post.timestamp,
            "already_liked": post.is_already_liked_by(user),
            "editable": post.is_editable_by(user),
        })

    return JsonResponse(posts, safe=False, status=200)


@login_required
def user_posts(request, user_id):
    try:
        user = User.objects.get(id=request.user.id)

        post_user = User.objects.get(id=user_id)
        post_objects = Post.objects.filter(user=post_user).order_by("-timestamp")

    except User.DoesNotExist:
        return JsonResponse({"error": "User not Found"}, status=404)

    posts = []
    for post in post_objects:
        posts.append({
            "id": post.id,
            "user_id": post.user.id,
            "username": post.user.username,
            "content": post.content,
            "likes": post.likes_num(),
            "timestamp": post.timestamp,
            "already_liked": post.is_already_liked_by(user),
            "editable": post.is_editable_by(user),
        })
    return JsonResponse(posts, safe=False, status=200)


def following_post(request):

    user = User.objects.get(id=request.user.id)
    return


@csrf_exempt
@login_required
def like_post(request):

    # only POST request is allowed
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    data = json.loads(request.body)
    post_id = data.get("post_id", "")

    # try to query for user and post in database and return error if not found
    try:
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=post_id)

    except User.DoesNotExist:
        return JsonResponse({"error": "User Not found!"}, status=404)

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found!"}, status=404)
    
    # check if user has already liked the post or not
    if post.is_already_liked_by(user):
        post.likes.remove(user)
        post.save()
        action_done = "Unliked"
    else:
        post.likes.add(user)
        post.save()
        action_done = "Liked"

    result = {
        "message": f"Post {action_done} successfully!",
        "likes_count": post.likes_num(),
    }

    return JsonResponse(result, status=200)


@login_required
def profile_info(request, user_id):
    
    if user_id == 0:
        user_id = request.user.id

    try:
        profile_user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=profile_user)

        user = User.objects.get(id=request.user.id)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not Found!"}, status=404)

    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found!"}, status=404)

    result = {
        "user_id": profile.user.id,
        "username": profile.user.username,
        "is_valid_follow": profile.is_valid_follow(user),
        "is_already_follower": profile.is_already_follower(user), 
        "followers_num": profile.followers_num(),
        "following_num": profile.following_num(),
    }

    return JsonResponse(result, status=200)


@csrf_exempt
@login_required
def follow(request):

    if request.method != "POST":
        return JsonResponse({"error": "Request must be via POST"}, status=400)
    
    data = json.loads(request.body)
    user_id = data.get("user_id", "")

    try:
        another_user = User.objects.get(id=user_id)
        another_profile = Profile.objects.get(user=another_user)

        user = User.objects.get(id=request.user.id)
        user_profile = Profile.objects.get(user=user)
            
    except User.DoesNotExist or Profile.DoesNotExist:
        return JsonResponse({"error": "User not found!"}, status=404)

    if user_profile.is_already_following(another_user):  
        user_profile.following.remove(another_user)
        another_profile.followers.remove(user)
        action_done = "unfollowed"
    
    else:
        user_profile.following.add(another_user)
        another_profile.followers.add(user)
        action_done = "followed"
    
    user_profile.save()
    another_profile.save()

    result = {
        "message": f"Profile {action_done} sucessfully!",
        "followers_num": another_profile.followers_num(),
        "following_num": another_profile.following_num(),
    }

    return JsonResponse(result, status=200)


@csrf_exempt
@login_required
def edit_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "Request must be via POST!"}, status=400)

    data = json.loads(request.body)
    post_id = data.get("post_id", "")
    content = data.get("content", "")

    try:
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=post_id)

    except User.DoesNotExist:
        return JsonResponse({"error": "User Not found!"}, status=404)

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found!"}, status=404)

    if post.is_editable_by(user):
        post.content = content
        post.save()

        result = {
            "message": "Post editted successfully!", 
            "user_id": request.user.id,
        }
        return JsonResponse(result, status=200)
    
    return JsonResponse({"error": "User has no permission to edit the post!"}, status=400)