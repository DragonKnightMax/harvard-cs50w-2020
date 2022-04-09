from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="profile")
    following = models.ManyToManyField("User", blank=True, related_name="is_following")
    followers = models.ManyToManyField("User", blank=True, related_name="followed_by")

    def __str__(self):
        return self.user.username

    def followers_num(self):
        return self.followers.count()

    def following_num(self):
        return self.following.count()

    def is_valid_follow(self, user):
        if user == self.user:
            return False
        return True

    def is_already_following(self, user):
        if user in self.following.all():
            return True
        return False

    def is_already_follower(self, user):
        if user in self.followers.all():
            return True
        return False


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts_added")
    content = models.CharField(max_length=500)
    likes = models.ManyToManyField("User", blank=True, related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def likes_num(self):
        return self.likes.count()

    def is_already_liked_by(self, user):
        if user in self.likes.all():
            return True
        return False

    def is_editable_by(self, user):
        if user == self.user:
            return True
        return False