from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),

    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path(
        "comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment"
    ),

    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),

  path(
    "profile/edit/",
    views.edit_profile,
    name="edit_profile"
),

path(
    "profile/<str:username>/follow/",
    views.toggle_follow,
    name="toggle_follow"
),

path(
    "profile/<str:username>/",
    views.profile,
    name="profile"
),
]