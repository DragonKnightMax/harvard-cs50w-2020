from django.urls import path
from . import views

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView


urlpatterns = [
    # Handle favicon.ico 404 not found in browser (worked)
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('encyclopedia/favicon.ico'))),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("save", views.saveEdit, name="saveEdit"),
    path("random", views.random, name="random")
]