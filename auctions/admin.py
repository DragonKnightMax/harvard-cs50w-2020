from django.contrib import admin
from .models import Listing, Comment, Watchlist, Category, User

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "description", "price", "image_url", "category", "date_time", "status", "winner")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "comment", "date_time")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user")


# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Category)
admin.site.register(User)