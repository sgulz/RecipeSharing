from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Tag, RecipeIngredient, RecipeTag
from Recipe.application import RecipeApplication

# Create your tests here.
class RecipeTest(TestCase):
    def setUp(self):
        self.recipeApplication = RecipeApplication()

    def compareRecipeProperties(self, recipe1, title, description, instructions, duration, servings, calories):
        # Compares the properties of two recipes
        self.assertEqual(recipe1.title, title)
        self.assertEqual(recipe1.description, description)
        self.assertEqual(recipe1.instructions, instructions)
        self.assertEqual(recipe1.duration, duration)
        self.assertEqual(recipe1.servings, servings)
        self.assertEqual(recipe1.calories, calories)

    def testGetOrCreateTag(self):
        # Tests if a tag can be created successfully
        tagName = 'Test Tag'
        tag = self.recipeApplication.getOrCreateTag(tagName)
        self.assertIsNotNone(tag)
        self.assertEqual(tag.name, tagName)
        self.assertTrue(Tag.objects.filter(name=tagName).exists())

    def testGetOrCreateIngredient(self):
        # Tests if an ingredient can be created successfully
        ingredientName = 'Test Ingredient'
        ingredient = self.recipeApplication.getOrCreateIngredient(ingredientName)
        self.assertIsNotNone(ingredient)
        self.assertEqual(ingredient.name, ingredientName)
        self.assertTrue(Ingredient.objects.filter(name=ingredientName).exists())

    def testCreateRecipe(self):
        # Tests if a recipe can be created successfully
        recipeProperties = {
            'title': 'Test Recipe',
            'description': 'This is a test recipe.',
            'instructions': 'Mix ingredients and bake.',
            'duration': 30,
            'servings': 4,
            'calories': 200
        }
        self.recipeApplication.createRecipe(
            author=User.objects.create(username="testuser"),
            **recipeProperties
        )
        recipe = self.recipeApplication.getRecipe(1)
        self.compareRecipeProperties(recipe, **recipeProperties)

    def testGetRecipe(self):
        # Tests if a recipe can be retrieved successfully
        recipeProperties = {
            'title': 'Test Recipe',
            'description': 'This is a test recipe.',
            'instructions': 'Mix ingredients and bake.',
            'duration': 30,
            'servings': 4,
            'calories': 200
        }
        self.recipeApplication.createRecipe(
            author=User.objects.create(username="testuser"),
            **recipeProperties
        )
        recipe = self.recipeApplication.getRecipe(1)
        self.assertIsNotNone(recipe)
        self.compareRecipeProperties(recipe, **recipeProperties)

    def testGetAllRecipes(self):
        # Tests if all recipes can be retrieved successfully
        recipeProperties1 = {
            'title': 'Test Recipe 1',
            'description': 'This is the first test recipe.',
            'instructions': 'Mix ingredients and bake.',
            'duration': 30,
            'servings': 4,
            'calories': 200
        }
        recipeProperties2 = {
            'title': 'Test Recipe 2',
            'description': 'This is the second test recipe.',
            'instructions': 'Mix ingredients and bake.',
            'duration': 45,
            'servings': 6,
            'calories': 300
        }
        self.recipeApplication.createRecipe(
            author=User.objects.create(username="testuser1"),
            **recipeProperties1
        )
        self.recipeApplication.createRecipe(
            author=User.objects.create(username="testuser2"),
            **recipeProperties2
        )
        recipes = self.recipeApplication.getAllRecipes()
        self.assertEqual(len(recipes), 2)
        self.compareRecipeProperties(recipes[0], **recipeProperties1)
        self.compareRecipeProperties(recipes[1], **recipeProperties2)
    
    def testAddTagToRecipe(self):
        # Tests if a tag can be added to a recipe successfully
        recipe = Recipe.objects.create(
            author=User.objects.create(username="testuser"),
            title='Test Recipe',
            description='This is a test recipe.',
            instructions='Mix ingredients and bake.',
            duration=30,
            servings=4,
            calories=200
        )
        tag = Tag.objects.create(name='Test Tag')
        self.recipeApplication.addTagToRecipe(recipe, tag)
        self.assertTrue(RecipeTag.objects.filter(recipe=recipe, tag=tag).exists())

    def testAddIngredientToRecipe(self):
        # Tests if an ingredient can be added to a recipe successfully
        recipe = Recipe.objects.create(
            author=User.objects.create(username="testuser"),
            title='Test Recipe',
            description='This is a test recipe.',
            instructions='Mix ingredients and bake.',
            duration=30,
            servings=4,
            calories=200
        )
        ingredient = Ingredient.objects.create(name='Test Ingredient')
        self.recipeApplication.addIngredientToRecipe(recipe, ingredient, 1, 'unit')
        self.assertTrue(RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient).exists())
    
    def testRemoveTagFromRecipe(self):
        # Tests if a tag can be removed from a recipe successfully
        recipe = Recipe.objects.create(
            author=User.objects.create(username="testuser"),
            title='Test Recipe',
            description='This is a test recipe.',
            instructions='Mix ingredients and bake.',
            duration=30,
            servings=4,
            calories=200
        )
        tag = Tag.objects.create(name='Test Tag')
        self.recipeApplication.addTagToRecipe(recipe, tag)
        self.recipeApplication.removeTagFromRecipe(recipe, tag)
        self.assertFalse(RecipeTag.objects.filter(recipe=recipe, tag=tag).exists())

    def testRemoveIngredientFromRecipe(self):
        # Tests if an ingredient can be removed from a recipe successfully
        recipe = Recipe.objects.create(
            author=User.objects.create(username="testuser"),
            title='Test Recipe',
            description='This is a test recipe.',
            instructions='Mix ingredients and bake.',
            duration=30,
            servings=4,
            calories=200
        )
        ingredient = Ingredient.objects.create(name='Test Ingredient')
        self.recipeApplication.addIngredientToRecipe(recipe, ingredient, 1, 'unit')
        self.recipeApplication.removeIngredientFromRecipe(recipe, ingredient)
        self.assertFalse(RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient).exists())

    def testGetRecipeTags(self):
        # Tests if tags can be retrieved from a recipe successfully
        recipe = Recipe.objects.create(
            author=User.objects.create(username="testuser"),
            title='Test Recipe',
            description='This is a test recipe.',
            instructions='Mix ingredients and bake.',
            duration=30,
            servings=4,
            calories=200
        )
        tag = Tag.objects.create(name='Test Tag')
        self.recipeApplication.addTagToRecipe(recipe, tag)
        tags = self.recipeApplication.getRecipeTags(recipe)
        self.assertTrue(RecipeTag.objects.filter(recipe=recipe, tag=tag).exists())
    
    def testGetRecipeIngredients(self):
        # Tests if ingredients can be retrieved from a recipe successfully
        recipe = Recipe.objects.create(
            author=User.objects.create(username="testuser"),
            title='Test Recipe',
            description='This is a test recipe.',
            instructions='Mix ingredients and bake.',
            duration=30,
            servings=4,
            calories=200
        )
        ingredient = Ingredient.objects.create(name='Test Ingredient')
        self.recipeApplication.addIngredientToRecipe(recipe, ingredient, 1, 'unit')
        ingredients = self.recipeApplication.getRecipeIngredients(recipe)
        self.assertTrue(RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient).exists())


    def testGetUsersRecipes(self):
        # Tests if recipes can be retrieved for a user successfully
        user1 = User.objects.create(username="testuser1")
        recipeProperties1 = {
            'title': 'Test Recipe 1',
            'description': 'This is the first test recipe.',
            'instructions': 'Mix ingredients and bake.',
            'duration': 30,
            'servings': 4,
            'calories': 200
        }
        user2 = User.objects.create(username="testuser2")
        recipeProperties2 = {
            'title': 'Test Recipe 2',
            'description': 'This is the second test recipe.',
            'instructions': 'Mix ingredients and bake.',
            'duration': 45,
            'servings': 6,
            'calories': 300
        }
        self.recipeApplication.createRecipe(
            author=user1,
            **recipeProperties1
        )
        self.recipeApplication.createRecipe(
            author=user2,
            **recipeProperties2
        )
        recipes1 = self.recipeApplication.getUsersRecipes(user1)
        recipes2 = self.recipeApplication.getUsersRecipes(user2)
        self.assertFalse(recipes1 == recipes2)