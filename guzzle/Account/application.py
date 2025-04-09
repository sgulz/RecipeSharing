# Application Layer of the Layered architecture
# Handles moving data between Business and Data Layers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class AccountApplication:
    def __init__(self):
        self.userID = None

    def getUserID(self):
        return self.userID

    def setUserID(self, userID):
        self.userID = userID

    def getUsername(self, user=None):
        return User.get_username() if user is None else user.get_username()

    def checkPassword(self, password, user=None):
        return User.check_password(password) if user is None else user.check_password(password)

    def createAccount(self, username: str, password: str) -> bool:
        try:
            print("Creating account")
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return True
        except:
            return False
        
    def login(self, request, username: str, password: str) -> bool:
        user = authenticate(username=username, password=password)
        if user is not None:
            print("Logging in")
            login(request, user)
            return True
        else:
            return False
        
    def logout(self, request):
        if request.user.is_authenticated:
            print("Logging out")
            logout(request)
            return True
        else:
            return

    def deleteAccount(self, user=None):
        if user is None:
            print("Deleting account")
            User.delete()
        else:
            user.delete()
    