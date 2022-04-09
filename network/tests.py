from django.test import TestCase, Client
from.models import User, Profile, Post

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):

        user1 = User.objects.create(username="frankie", email="heidragon3045@example.com", password="29879dbef5")
        user2 = User.objects.create(username="heidragon", email="alibaba123@example.com", password="qwerty")
        user3 = User.objects.create(username="xyz", email="xyz@example.com", password="12345")
        user4 = User.objects.create(username="abcdef", email="abc@example.com", password="abcdef")

        profile1 = Profile.objects.create(user=user1)
        profile2 = Profile.objects.create(user=user2)
        profile3 = Profile.objects.create(user=user3)

        post1 = Post.objects.create(user=user1, content="This is post 1")
        post2 = Post.objects.create(user=user2, content="This is post 2")


    def test_already_like_post(self):
        """Check that user already liked a post"""
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)

        post1 = Post.objects.get(user=user1)
        post1.likes.add(user2)
        post1.save()

        self.assertTrue(post1.is_already_liked_by(user2))


    def test_post_like_count(self):
        """Check that post 1 likes count is 2, regardless of post 2 likes count"""
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user3 = User.objects.get(id=3)

        post1 = Post.objects.get(user=user1)
        post1.likes.add(user2)
        post1.likes.add(user3)
        post1.save()
        
        post2 = Post.objects.get(user=user2)
        post2.likes.add(user1)
        post2.likes.add(user3)
        post2.save()

        self.assertEqual(post1.likes_num(), 2)


    def test_post_unlike_count(self):
        """Check that post 1 likes count is 1, after user has unliked a post"""
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user3 = User.objects.get(id=3)

        post1 = Post.objects.get(user=user1)
        post1.likes.add(user2)
        post1.likes.add(user3)
        post1.likes.remove(user2)
        post1.save()

        self.assertEqual(post1.likes_num(), 1)


    def test_invalid_followers(self):
        """Check that user profile followers contain the user himself is invalid (False)"""
        user1 = User.objects.get(id=1)
        profile1 = Profile.objects.get(user=user1)

        self.assertFalse(profile1.is_valid_follow(user1))


    def test_invalid_following(self):
        """Check that the user following his profile is invalid (False)"""
        user1 = User.objects.get(id=1)
        profile1 = Profile.objects.get(user=user1)

        self.assertFalse(profile1.is_valid_follow(user1))


    def test_already_follower(self):
        """Check that the user is already following another user"""
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)

        profile1 = Profile.objects.get(user=user1)
        profile1.followers.add(user2)
        profile1.save()

        self.assertTrue(profile1.is_already_follower(user2))


    def test_already_following(self):
        """Check that the user is already following another user"""
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)

        profile2 = Profile.objects.get(user=user2)
        profile2.following.add(user1)
        profile2.save()

        self.assertTrue(profile2.is_already_following(user1))


    def test_followers_count(self):
        """Check that profile followers is 2"""
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user3 = User.objects.get(id=3)

        profile1 = Profile.objects.get(user=user1)
        profile1.followers.add(user2)
        profile1.followers.add(user3)

        self.assertEqual(profile1.followers_num(), 2)


    def test_following_count(self):
        """Check that the profile that a user is currently following is 1 """
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)

        profile2 = Profile.objects.get(user=user2)
        profile2.followers.add(user1)

        profile1 = Profile.objects.get(user=user1)
        profile1.following.add(user2)

        self.assertEqual(profile1.following_num(), 1)


    def test_post_is_editable_by_poster(self):
        """Check that post is editable by poster"""
        user1 = User.objects.get(id=1)
        post1 = Post.objects.get(user=user1)

        self.assertTrue(post1.is_editable_by(user1))