"""
URL configuration for guzzle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
  
from django.contrib import admin
from django.urls import path
from Home import views as homeViews
from Account import views as accountViews
from Recipe import views as recipeViews
from Friends import views as friendsViews

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homeViews.home, name="home"),
    path("signup/", accountViews.signup, name="signup"),
    path("login/", accountViews.login, name="login"),
    path("signout/", accountViews.signout, name="signout"),
    path("createRecipe/", recipeViews.createRecipe, name="createRecipe"),
    path("myRecipes/", recipeViews.myRecipes, name="myRecipes"),
    path('recipe/<int:id>/view/', recipeViews.viewRecipe, name='viewRecipe'),
    path('registerTag/', recipeViews.registerTag, name='registerTag'),
    path('registerIngredient/', recipeViews.registerIngredient, name='registerIngredient'),
    path("friends/", friendsViews.myFriends, name="myFriends"),
    path("addFriend/", friendsViews.addFriend, name="addFriend"),
    path("acceptFriendRequest/<int:requestID>/", friendsViews.acceptFriendRequest, name="acceptFriendRequest"),
    path("rejectFriendRequest/<int:requestID>/", friendsViews.rejectFriendRequest, name="rejectFriendRequest"),
    path("cancelFriendRequest/<int:requestID>/", friendsViews.cancelFriendRequest, name="cancelFriendRequest"),
    path("removeFriend/<int:friendID>/", friendsViews.removeFriend, name="removeFriend"),
    path('recipe/<int:recipe_id>/favourite/', recipeViews.toggle_favourite, name='toggle_favourite'),
    path('my-favourites/', recipeViews.my_favourites, name='my_favourites'),
]
