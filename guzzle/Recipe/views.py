from django.shortcuts import render, redirect
from .application import RecipeApplication

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
    recipes = recipeApplication.getUsersRecipes(request.user) 
    for recipe in recipes:
        print(recipe.title)

    context = {'recipesEnum': enumerate(recipes)}
    return render(request, 'myRecipesPage.html', context)

def viewRecipe(request, id):
    recipe = recipeApplication.getRecipe(id)
    recipeTags = recipeApplication.getRecipeTags(recipe)
    recipeIngredients = recipeApplication.getRecipeIngredients(recipe)

    if request.method == 'POST':
        # Handle interactions (leave a comment, rate the recipe, etc.)
        pass

    context = {'recipe': recipe,
              'recipeTagsEnum': enumerate(recipeTags),
              'recipeIngredientsEnum': enumerate(recipeIngredients)}

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
