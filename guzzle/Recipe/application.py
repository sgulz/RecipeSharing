# Application Layer of the Layered architecture
# Handles moving data between Business and Data Layers

from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Tag, RecipeIngredient, RecipeTag

class RecipeApplication:
    def __init__(self):
        self.userID = None

    def getOrCreateTag(self, tagName: str):
        tag, created = Tag.objects.get_or_create(name=tagName)
        if created:
            print(f"Tag '{tagName}' created.")
        else:
            print(f"Tag '{tagName}' already exists.")
        return tag

    def getOrCreateIngredient(self, ingredientName: str):
        ingredient, created = Ingredient.objects.get_or_create(name=ingredientName)
        if created:
            print(f"Ingredient '{ingredientName}' created.")
        else:
            print(f"Ingredient '{ingredientName}' already exists.")
        return ingredient


    def createRecipe(self, author: User, title: str, description: str, instructions: str, duration: int, servings: int, calories: int):
        try:
            print("Creating recipe")
            recipe = Recipe(author=author, title=title, description=description, instructions=instructions, duration=duration, servings=servings, calories=calories)
            recipe.save()
            return recipe
        except Exception as e:
            print("Error creating recipe:", e)
            return False

    def getRecipe(self, recipeID: int):
        try:
            print("Getting recipe")
            recipe = Recipe.objects.get(id=recipeID)
            return recipe
        except Exception as e:
            print("Error getting recipe:", e)
            return None
        
    def getUsersRecipes(self, author: User):
        try:
            print("Getting user's recipes")
            recipes = Recipe.objects.filter(author=author)
            return recipes
        except Exception as e:
            print("Error getting user's recipes:", e)
            return None

    def getAllRecipes(self):
        try:
            print("Getting all recipes")
            recipes = Recipe.objects.all()
            return recipes
        except Exception as e:
            print("Error getting recipes:", e)
            return None
    
    def createIngredient(self, name: str) -> bool:
        try:
            print("Creating ingredient")
            ingredient = Ingredient(name=name)
            ingredient.save()
            return True
        except:
            return False

    def getAllIngredients(self):
        try:
            print("Getting all ingredients")
            ingredients = Ingredient.objects.all()
            return ingredients
        except Exception as e:
            print("Error getting ingredients:", e)
            return None
    
    def getIngredient(self, ingredientID: int):
        try:
            print("Getting ingredient")
            ingredient = Ingredient.objects.get(id=ingredientID)
            return ingredient
        except Exception as e:
            print("Error getting ingredient:", e)
            return None

    def createTag(self, name: str) -> bool:
        try:
            print("Creating tag")
            tag = Tag(name=name)
            tag.save()
            return True
        except:
            return False

    def getAllTags(self):
        try:
            print("Getting all tags")
            tags = Tag.objects.all()
            return tags
        except Exception as e:
            print("Error getting tags:", e)
            return None
    
    def getTag(self, tagID: int):
        try:
            print("Getting tag")
            tag = Tag.objects.get(id=tagID)
            return tag
        except Exception as e:
            print("Error getting tag:", e)
            return None

    def addIngredientToRecipe(self, recipe, ingredient, quantity: float, unit: str) -> bool:
        try:
            print("Adding ingredient to recipe")
            recipeIngredient = RecipeIngredient(recipe=recipe, ingredient=ingredient, quantity=quantity, unit=unit)
            recipeIngredient.save()
            return True
        except Exception as e:
            print("Error adding ingredient to recipe:", e)
            return False 
    
    def removeIngredientFromRecipe(self, recipe, ingredient) -> bool:
        try:
            print("Removing ingredient from recipe")
            recipeIngredient = RecipeIngredient.objects.get(recipe=recipe, ingredient=ingredient)
            recipeIngredient.delete()
            return True
        except:
            return False

    def getRecipeIngredients(self, recipe) -> list:
        try:
            print("Getting recipe ingredients")
            recipeIngredients = RecipeIngredient.objects.filter(recipe=recipe)
            return recipeIngredients
        except Exception as e:
            print("Error getting recipe ingredients:", e)
            return None

    def addTagToRecipe(self, recipe, tag) -> bool:
        try:
            print("Adding tag to recipe")
            recipeTag = RecipeTag(recipe=recipe, tag=tag)
            recipeTag.save()
            return True
        except Exception as e:
            print("Error adding tag to recipe:", e)
            return False

    def removeTagFromRecipe(self, recipe, tag) -> bool:
        try:
            print("Removing tag from recipe")
            recipeTag = RecipeTag.objects.get(recipe=recipe, tag=tag)
            recipeTag.delete()
            return True
        except Exception as e:
            print("Error removing tag from recipe:", e)
            return False

    def getRecipeTags(self, recipe) -> list:
        try:
            print("Getting recipe tags")
            recipeTags = RecipeTag.objects.filter(recipe=recipe)
            return recipeTags
        except Exception as e:
            print("Error getting recipe tags:", e)
            return None