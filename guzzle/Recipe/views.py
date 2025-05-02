from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .application import RecipeApplication
from .models import Recipe

recipeApplication = RecipeApplication()

def createRecipe(request):
    # Get all existing tags from the database
    tags = recipeApplication.getAllTags()
    ingredients = recipeApplication.getAllIngredients()
    context = {'tagsEnum': enumerate(tags),
               'ingredientsEnum': enumerate(ingredients)}

    if request.method == 'POST' and request.POST.get('formType') == 'createRecipe':
        title = request.POST['title']
        instructions = request.POST['instructions']
        description = request.POST['description']
        duration = request.POST['duration']
        servings = request.POST['servings']
        calories = request.POST['calories']
        selectedTagIDs = request.POST.getlist('tags')
        selectedIngredientIDs = request.POST.getlist('ingredients')

        recipe = recipeApplication.createRecipe(
            author=request.user,
            title=title,
            description=description,
            instructions=instructions,
            duration=duration,
            servings=servings,
            calories=calories,
        )

        # Associate selected tags with the recipe
        for tagID in selectedTagIDs:
            print('tagID', tagID)
            tag = recipeApplication.getTag(tagID)
            recipeApplication.addTagToRecipe(recipe, tag)

        # Associate ingredients with the recipe
        for ingredientID in selectedIngredientIDs:
            print('ingredientID', ingredientID)
            ingredient = recipeApplication.getIngredient(ingredientID)
            # quantity = request.POST['quantity_' + ingredientID]
            # unit = request.POST['unit_' + ingredientID]
            quantity = 1
            unit = 'unit'
            recipeApplication.addIngredientToRecipe(recipe, ingredient, quantity, unit)

        return redirect('myRecipes')

    return render(request, 'createRecipePage.html', context)

def myRecipes(request):
    if request.user.is_authenticated:
        recipes = recipeApplication.getUsersRecipes(request.user)
        for recipe in recipes:
            print(recipe.title)

        context = {
            'recipesEnum': enumerate(recipes),
            'recipes': recipes,  # Added this line
            'user': request.user
        }
        return render(request, 'myRecipesPage.html', context)
    return redirect('login')

def viewRecipe(request, id):
    recipe = recipeApplication.getRecipe(id)
    recipeTags = recipeApplication.getRecipeTags(recipe)
    recipeIngredients = recipeApplication.getRecipeIngredients(recipe)
    is_favourited = recipe.favourites.filter(id=request.user.id).exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        # Handle interactions (leave a comment, rate the recipe, etc.)
        pass

    context = {
        'recipe': recipe,
        'recipeTagsEnum': enumerate(recipeTags),
        'recipeIngredientsEnum': enumerate(recipeIngredients),
        'is_favourited': is_favourited,
        'favourite_count': recipe.favourite_count()
    }

    for tag in recipeTags:
        print(tag.tag.name)
    print(context)
    return render(request, 'viewRecipePage.html', context)

def registerTag(request):
    if request.method == 'POST':
        tagName = request.POST.get('tagName')
        if tagName:
            recipeApplication.getOrCreateTag(tagName=tagName)
    return redirect('createRecipe')

def registerIngredient(request):
    if request.method == 'POST':
        ingredientName = request.POST.get('ingredientName')
        if ingredientName:
            recipeApplication.getOrCreateIngredient(ingredientName=ingredientName)
    return redirect('createRecipe')

@login_required
def toggle_favourite(request, recipe_id):
    recipe = recipeApplication.getRecipe(recipe_id)
    if not recipe:
        return JsonResponse({'error': 'Recipe not found'}, status=404)

    is_favourited = recipe.favourites.filter(id=request.user.id).exists()
    if is_favourited:
        recipe.favourites.remove(request.user)
        status = 'removed'
    else:
        recipe.favourites.add(request.user)
        status = 'added'

    return JsonResponse({
        'status': status,
        'count': recipe.favourite_count()
    })

@login_required
def my_favourites(request):
    favourite_recipes = Recipe.objects.filter(favourites=request.user)
    context = {
        'recipesEnum': enumerate(favourite_recipes),
        'recipes': favourite_recipes,  # Added this line
        'user': request.user
    }
    return render(request, 'myFavouritesPage.html', context)