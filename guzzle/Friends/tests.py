from django.test import TestCase
from django.contrib.auth.models import User
from Friends.application import FriendsApplication
from Friends.models import Friend

# Create your tests here.
class FriendsTest(TestCase):
    def setUp(self):
        self.friendsApplication = FriendsApplication()

    def testAddFriend(self):
        user1 = User.objects.create_user(username="test", password="test")
        user2 = User.objects.create_user(username="test2", password="test2")
        self.friendsApplication.addFriend(user1, user2)
        self.assertTrue(Friend.objects.filter(user=user1).exists())

    def testAreFriends(self):
        user1 = User.objects.create_user(username="test", password="test")
        user2 = User.objects.create_user(username="test2", password="test2")
        user3 = User.objects.create_user(username="test3", password="test3")
        self.friendsApplication.addFriend(user1, user2)
        self.assertTrue(self.friendsApplication.areFriends(user1, user2))
        self.assertFalse(self.friendsApplication.areFriends(user1, user3))

    def testAcceptFriendRequest(self):
        user1 = User.objects.create_user(username="test", password="test")
        user2 = User.objects.create_user(username="test2", password="test2")
        self.friendsApplication.addFriend(user1, user2)
        self.friendsApplication.acceptFriendRequest(1)
        self.assertTrue(Friend.objects.filter(user=user1, friend=user2, status="accepted").exists())
    
    def testRejectFriendRequest(self):
        user1 = User.objects.create_user(username="test", password="test")
        user2 = User.objects.create_user(username="test2", password="test2")
        self.friendsApplication.addFriend(user1, user2)
        self.friendsApplication.rejectFriendRequest(1)
        self.assertTrue(Friend.objects.filter(user=user1, friend=user2, status="rejected").exists())

    def testCancelFriendRequest(self):
        user1 = User.objects.create_user(username="test", password="test")
        user2 = User.objects.create_user(username="test2", password="test2")
        self.friendsApplication.addFriend(user1, user2)
        self.friendsApplication.cancelFriendRequest(1)
        self.assertFalse(Friend.objects.filter(user=user1, friend=user2))

    def testGetFriends(self):
        user1 = User.objects.create_user(username="test", password="test")
        user2 = User.objects.create_user(username="test2", password="test2")
        user3 = User.objects.create_user(username="test3", password="test3")
        self.friendsApplication.addFriend(user1, user2)
        self.friendsApplication.addFriend(user1, user3)
        self.friendsApplication.acceptFriendRequest(1)
        self.friendsApplication.acceptFriendRequest(2)
        self.assertEqual(len(self.friendsApplication.getFriends(user1)), 2)

    def testGetIncomingRequests(self):
        user1 = User.objects.create_user(username="test", password="test")
        user2 = User.objects.create_user(username="test2", password="test2")
        user3 = User.objects.create_user(username="test3", password="test3")
        self.friendsApplication.addFriend(user1, user3)
        self.friendsApplication.addFriend(user2, user3)
        self.assertEqual(len(self.friendsApplication.getIncomingRequests(user3)), 2)
    
    def testGetOutgoingRequests(self):
        user1 = User.objects.create_user(username="test", password="test")
        user2 = User.objects.create_user(username="test2", password="test2")
        user3 = User.objects.create_user(username="test3", password="test3")
        self.friendsApplication.addFriend(user1, user2)
        self.friendsApplication.addFriend(user1, user3)
        self.assertEqual(len(self.friendsApplication.getOutgoingRequests(user1)), 2)