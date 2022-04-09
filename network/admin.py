from django.contrib import admin
from .models import User, Post, Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
