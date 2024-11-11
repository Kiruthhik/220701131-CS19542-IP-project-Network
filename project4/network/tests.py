from django.test import TestCase
from network.models import *

# Create your tests here.

class followersTest(TestCase):
    def setUp(self):
        User.objects.create(username = "tester1", email = "tester1@gmail.com")
        User.objects.create(username = "tester2", email = "tester2@gmail.com")
        self.user1 = User.objects.get(username = "tester1")
        self.user2 = User.objects.get(username = "tester2")
        self.user1.following.add(self.user2)

    def test_follow_relation(self):
        #self.assertTrue(user2.followers.filter(user = user1).exists())
        #self.assertTrue(user1.following.filter(user = user2).exists())
        print("testing following ....\n")
        self.assertTrue(self.user2 in self.user1.following.all())
        self.assertTrue(self.user1 in self.user2.followers.all())

    def test_unfollow_relation(self):
        print("testing unfollowing...\n")
        self.user1.following.remove(self.user2)
        self.assertFalse(self.user2 in self.user1.following.all())
        self.assertFalse(self.user1 in self.user2.followers.all())

class likeTest(TestCase):
    def setUp(self):
        self.tester1 = User.objects.create(username = "tester1", email="testeer1@gmail.com")
        self.tester2 = User.objects.create(username = "tester2", email="testeer2@gmail.com")
        self.post = Post.objects.create(content="test post",posted_by=self.tester1)

    def test_like(self):
        self.post.liked_by.add(self.tester2)
        print("testing like functionality....\n")
        self.assertTrue(self.tester2 in self.post.liked_by.all())
        self.assertTrue(self.post in self.tester2.liked.all())

    def test_unlike(self):
        self.post.liked_by.remove(self.tester2)
        print("testing unlike...\n")
        self.assertFalse(self.tester2 in self.post.liked_by.all())
        self.assertFalse(self.post in self.tester2.liked.all())
        self.post.content = "testing post edit functionality"
        self.post.save()
        print("testing edit functionality....\n")
        self.assertTrue(self.post.content == "testing post edit functionality")
        self.assertFalse(self.tester2 in self.post.liked_by.all())
        self.assertFalse(self.post in self.tester2.liked.all())

    def edit_post(self):
        self.post.content = "testing post edit functionality"
        self.post.save()
        print("testing edit functionality....\n")
        self.assertTrue(self.post.content == "testing post edit functionality")
        self.assertFalse(self.tester2 in self.post.liked_by.all())
        self.assertFalse(self.post in self.tester2.liked.all())

