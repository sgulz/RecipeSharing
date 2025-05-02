# Application Layer of the Layered architecture
# Handles moving data between Business and Data Layers

from django.contrib.auth.models import User
from django.db import models
from .models import Friend

class FriendsApplication:
    def __init__(self):
        pass

    def addFriend(self, user: User, friendUsername: User) -> bool:
        try:
            print(f"Sending friend request from {user.username} to {friendUsername}")
            # Check if the friend exists
            try:
                friend = User.objects.get(username=friendUsername)
            except User.DoesNotExist:
                print(f"User {friendUsername} does not exist")
                return False
            
            # Check if the user is trying to add themselves
            if user.id == friend.id:
                print("Cannot send friend request to yourself")
                return False
            
            # Check if a friendship already exists (in either direction)
            requestExists = self.areFriends(user, friend)
            if requestExists:
                print(f"Friendship already exists with status: {requestExists}")
                return False
            
            friendRequest = Friend(user=user, friend=friend, status='pending')
            friendRequest.save()
            return True
        except Exception as e:
            print(f"Error sending friend request: {e}")
            return False

    def acceptFriendRequest(self, requestID: int) -> bool:
        try:
            print(f"Accepting friend request {requestID}")
            request = Friend.objects.get(id=requestID)
            request.status = 'accepted'
            request.save()
            return True
        except Exception as e:
            print(f"Error accepting friend request: {e}")
            return False

    def rejectFriendRequest(self, requestID: int) -> bool:
        try:
            print(f"Rejecting friend request {requestID}")
            request = Friend.objects.get(id=requestID)
            request.delete()
            return True
        except Exception as e:
            print(f"Error rejecting friend request: {e}")
            return False

    def cancelFriendRequest(self, requestID: int) -> bool:
        try:
            print(f"Canceling friend request {requestID}")
            request = Friend.objects.get(id=requestID)
            request.delete()
            return True
        except Exception as e:
            print(f"Error canceling friend request: {e}")
            return False

    def removeFriend(self, user: User, friend: User) -> bool:
        try:
            print(f"Removing friendship between {user.username} and {friend.username}")
            # Find and delete the friendship in either direction
            friendship_as_requester = Friend.objects.filter(user=user, friend=friend, status='accepted')
            friendship_as_receiver = Friend.objects.filter(user=friend, friend=user, status='accepted')
            
            if friendship_as_requester:
                print(f"Found friendship where {user.username} is the requester")
                friendship_as_requester.delete()
                return True
            elif friendship_as_receiver:
                print(f"Found friendship where {user.username} is the receiver")
                friendship_as_receiver.delete()
                return True
            else:
                print("Friendship not found in either direction")
                return False
        except Exception as e:
            print(f"Error removing friend: {e}")
            return False

    def getFriends(self, user: User):
        try:
            print(f"Getting friends for {user.username}")
            # Get friendships where the user is either the requester or the receiver
            sent_requests = Friend.objects.filter(user=user, status='accepted')
            received_requests = Friend.objects.filter(friend=user, status='accepted')
            
            # Extract the friend users from the friendship objects
            friends_from_sent = [friendship.friend for friendship in sent_requests]
            friends_from_received = [friendship.user for friendship in received_requests]
            
            # Combine the lists
            all_friends = friends_from_sent + friends_from_received
            
            return all_friends
        except Exception as e:
            print(f"Error getting friends: {e}")
            return []

    def getIncomingRequests(self, user: User) -> list:
        try:
            print(f"Getting incoming friend requests for {user.username}")
            requests = Friend.objects.filter(friend=user, status='pending')
            return requests
        except Exception as e:
            print(f"Error getting incoming friend requests: {e}")
            return []
    
    def getOutgoingRequests(self, user: User) -> list:
        try:
            print(f"Getting outgoing friend requests for {user.username}")
            requests = Friend.objects.filter(user=user, status='pending')
            return requests
        except Exception as e:
            print(f"Error getting outgoing friend requests: {e}")
            return []

    def areFriends(self, user1: User, user2: User) -> bool:
        try:
            requestExists = Friend.objects.filter(user=user1, friend=user2).exists() or Friend.objects.filter(user=user2, friend=user1).exists()
            
            return requestExists
        except Exception as e:
            print(f"Error checking friendship: {e}")
            return False
