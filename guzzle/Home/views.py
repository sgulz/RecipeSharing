from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from Recipe.application import RecipeApplication

recipeApplication = RecipeApplication()

def home(request):
    recipes = recipeApplication.getAllRecipes()
    context = {'recipes': recipes}
    for recipe in recipes:
        print(recipe.title)
    return render(request, 'homePage.html', context)