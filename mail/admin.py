from django.contrib import admin
from .models import User, Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "subject", "timestamp")

# Register your models here.
admin.site.register(User)
admin.site.register(Email, EmailAdmin)