from django.shortcuts import render, redirect
from django.urls import reverse
from Friends.application import FriendsApplication
from django.contrib.auth.models import User

friendsApplication = FriendsApplication()
# Create your views here.
def myFriends(request):
    friends = friendsApplication.getFriends(request.user)
    incomingRequests = friendsApplication.getIncomingRequests(request.user)
    outgoingRequests = friendsApplication.getOutgoingRequests(request.user)

    for request1 in incomingRequests:
        print('incoming request', request1.user.username, request1.friend.username)

    context = {
        'friends': friends,
        'incomingRequests': incomingRequests,
        'outgoingRequests': outgoingRequests,
        'error_message': request.session.pop('error_message', None),
        'success_message': request.session.pop('success_message', None)
    }
    return render(request,'myFriendsPage.html', context)

def addFriend(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            successful = friendsApplication.addFriend(request.user, username)
            if successful:
                request.session['success_message'] = f"Friend request sent to {username}!"
            else:
                request.session['error_message'] = f"Could not send friend request to {username}. User may not exist, or a request may already be pending."
    
    # Redirect to myFriends URL
    return redirect(reverse('myFriends'))

def acceptFriendRequest(request, requestID):
    if request.method == 'POST':
        friendsApplication.acceptFriendRequest(requestID)
        # Redirect to myFriends URL instead of calling the function directly
        return redirect(reverse('myFriends'))
    else:
        return redirect(reverse('myFriends'))
    
def rejectFriendRequest(request, requestID):
    if request.method == 'POST':
        friendsApplication.rejectFriendRequest(requestID)
        # Redirect to myFriends URL instead of calling the function directly
        return redirect(reverse('myFriends'))
    else:
        return redirect(reverse('myFriends'))
    
def cancelFriendRequest(request, requestID):
    if request.method == 'POST':
        friendsApplication.cancelFriendRequest(requestID)
        # Redirect to myFriends URL instead of calling the function directly
        return redirect(reverse('myFriends'))
    else:
        return redirect(reverse('myFriends'))
    
def removeFriend(request, friendID):
    if request.method == 'POST':
        try:
            friendUser = User.objects.get(id=friendID)
            friendsApplication.removeFriend(request.user, friendUser)
            
            # Redirect to myFriends URL instead of calling the function directly
            return redirect(reverse('myFriends'))
        
        except User.DoesNotExist:
            print(f"UserID {friendID} does not exist")
            return redirect(reverse('myFriends'))
    else:
        return redirect(reverse('myFriends'))