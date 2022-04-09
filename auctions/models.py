from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="", related_name="listing_owner")
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image_url = models.URLField(max_length=200, blank=True, null=True, default=None)
    category = models.CharField(max_length=64, blank=True, null=True, default=None)
    date_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=6, default="Active")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None, related_name="bid_winner")

    def __str__(self):
        return f"{self.id}: {self.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    comment = models.TextField()
    date_time = models.DateTimeField(auto_now=True)