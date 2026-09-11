from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile, Post, Comment, Like, Follow


def home(request):
    posts = Post.objects.select_related("author").prefetch_related(
        "comments",
        "likes"
    )

    if request.user.is_authenticated:
        Profile.objects.get_or_create(user=request.user)

    return render(
        request,
        "social/home.html",
        {"posts": posts}
    )


def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(
                request,
                "Please fill in all required fields."
            )
            return render(request, "social/register.html")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return render(request, "social/register.html")

        if len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters."
            )
            return render(request, "social/register.html")

        if User.objects.filter(username__iexact=username).exists():
            messages.error(
                request,
                "Username already exists. Please choose another username."
            )
            return render(request, "social/register.html")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                "Email is already registered. Please use another email."
            )
            return render(request, "social/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(user=user)

        login(request, user)

        messages.success(
            request,
            "Account created successfully!"
        )

        return redirect("home")

    return render(request, "social/register.html")


def user_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "social/login.html")


@login_required
def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


@login_required
def create_post(request):

    if request.method != "POST":
        return redirect("home")

    content = request.POST.get("content", "").strip()
    media = request.FILES.get("image")

    if not content and not media:
        messages.error(
            request,
            "Please write something or upload an image/video."
        )
        return redirect("home")

    if media:

        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".mp4",
            ".webm",
            ".mov",
            ".avi",
            ".mkv"
        ]

        file_name = media.name.lower()

        if not any(
            file_name.endswith(extension)
            for extension in allowed_extensions
        ):
            messages.error(
                request,
                "Only image and video files are allowed."
            )
            return redirect("home")

    Post.objects.create(
        author=request.user,
        content=content,
        image=media
    )

    messages.success(
        request,
        "Your post has been published!"
    )

    return redirect("home")


@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if post.author != request.user:
        messages.error(
            request,
            "You can only delete your own posts."
        )
        return redirect("home")

    if request.method == "POST":
        post.delete()

        messages.success(
            request,
            "Post deleted successfully."
        )

    return redirect("home")


@login_required
def add_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.method == "POST":

        content = request.POST.get(
            "content",
            ""
        ).strip()

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

        else:
            messages.error(
                request,
                "Comment cannot be empty."
            )

    return redirect("home")


@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if comment.author != request.user:
        messages.error(
            request,
            "You can only delete your own comments."
        )
        return redirect("home")

    if request.method == "POST":
        comment.delete()

        messages.success(
            request,
            "Comment deleted successfully."
        )

    return redirect("home")


@login_required
def toggle_like(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like = Like.objects.filter(
        post=post,
        user=request.user
    ).first()

    if like:
        like.delete()
    else:
        Like.objects.create(
            post=post,
            user=request.user
        )

    return redirect("home")


@login_required
def profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    profile_obj, created = Profile.objects.get_or_create(
        user=profile_user
    )

    posts = Post.objects.filter(
        author=profile_user
    ).select_related("author")

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    context = {
        "profile_user": profile_user,
        "profile_obj": profile_obj,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    }

    return render(
        request,
        "social/profile.html",
        context
    )


@login_required
def toggle_follow(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    if profile_user == request.user:
        messages.error(
            request,
            "You cannot follow yourself."
        )
        return redirect(
            "profile",
            username=username
        )

    follow = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).first()

    if follow:
        follow.delete()

        messages.success(
            request,
            f"You unfollowed {profile_user.username}."
        )

    else:
        Follow.objects.create(
            follower=request.user,
            following=profile_user
        )

        messages.success(
            request,
            f"You are now following {profile_user.username}."
        )

    return redirect(
        "profile",
        username=username
    )


@login_required
def edit_profile(request):

    profile_obj, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip()

        bio = request.POST.get(
            "bio",
            ""
        ).strip()

        profile_picture = request.FILES.get(
            "profile_picture"
        )

        if email:

            if User.objects.filter(
                email__iexact=email
            ).exclude(
                id=request.user.id
            ).exists():

                messages.error(
                    request,
                    "That email is already registered."
                )

                return render(
                    request,
                    "social/edit_profile.html",
                    {"profile_obj": profile_obj}
                )

            request.user.email = email
            request.user.save()

        profile_obj.bio = bio

        if profile_picture:

            allowed_extensions = [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".webp"
            ]

            file_name = profile_picture.name.lower()

            if not any(
                file_name.endswith(extension)
                for extension in allowed_extensions
            ):
                messages.error(
                    request,
                    "Please select a valid image file."
                )

                return render(
                    request,
                    "social/edit_profile.html",
                    {"profile_obj": profile_obj}
                )

            profile_obj.profile_picture = profile_picture

        profile_obj.save()

        messages.success(
            request,
            "Profile updated successfully!"
        )

        return redirect(
            "profile",
            username=request.user.username
        )

    return render(
        request,
        "social/edit_profile.html",
        {"profile_obj": profile_obj}
    )