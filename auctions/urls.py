from django.urls import path

from . import views

from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('auctions/favicon.ico'))),
    path("", views.index, name="index"),
    path("details/<str:listing_id>", views.details, name="details"),
    path("comment/<str:listing_id>", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<str:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<str:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("create", views.create_listing, name="create"),
    path("bid/<str:listing_id>", views.bid_item, name="bid_item"),
    path("close_auction/<str:listing_id>", views.close_auction, name="close_auction"),
    path("categories", views.categories, name="categories"),
    path("filterByCategory/<str:category>", views.filterByCategory, name="filterByCategory"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
