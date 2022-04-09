
from django.urls import path

from . import views

from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('network/favicon.ico'))),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts/new", views.new_post, name="new_post"),
    path("posts/all", views.all_post, name="all_post"),
    path("posts/<int:user_id>", views.user_posts, name="user_posts"),
    path("posts/like", views.like_post, name="like_post"),
    path("posts/edit", views.edit_post, name="edit_post"),
    path("posts/following", views.following_post, name="following_post"),
    path("profile/<int:user_id>", views.profile_info, name="profile_info"),
    path("profile/follow", views.follow, name="follow"),

]
