from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Recipe.models import Recipe, Ingredient, Tag, RecipeIngredient, RecipeTag
from Recipe.application import RecipeApplication
from Account.application import AccountApplication

class RecipeIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.recipeApplication = RecipeApplication()
        self.accountApplication = AccountApplication()
        
        # Create test user
        self.test_credentials = {
            'username': 'recipeIntegrationUser',
            'password': 'testPassword123'
        }
        self.accountApplication.createAccount(
            self.test_credentials['username'],
            self.test_credentials['password']
        )
        self.test_user = User.objects.get(username=self.test_credentials['username'])
        
    def test_recipe_creation_with_ingredients_and_tags(self):
        """Test creating a recipe with ingredients and tags"""
        # Create a recipe
        recipe = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Integration Test Recipe',
            description='Recipe for integration testing',
            instructions='Step 1: Test. Step 2: Verify.',
            duration=20,
            servings=2,
            calories=250
        )
        
        # Create and add ingredients
        ingredient1 = self.recipeApplication.getOrCreateIngredient('Test Ingredient 1')
        ingredient2 = self.recipeApplication.getOrCreateIngredient('Test Ingredient 2')
        
        self.recipeApplication.addIngredientToRecipe(recipe, ingredient1, 2, 'cups')
        self.recipeApplication.addIngredientToRecipe(recipe, ingredient2, 1, 'tbsp')
        
        # Create and add tags
        tag1 = self.recipeApplication.getOrCreateTag('TestTag1')
        tag2 = self.recipeApplication.getOrCreateTag('TestTag2')
        
        self.recipeApplication.addTagToRecipe(recipe, tag1)
        self.recipeApplication.addTagToRecipe(recipe, tag2)
        
        # Verify ingredients were added
        recipe_ingredients = self.recipeApplication.getRecipeIngredients(recipe)
        self.assertEqual(len(recipe_ingredients), 2)
        
        # Verify tags were added
        recipe_tags = self.recipeApplication.getRecipeTags(recipe)
        self.assertEqual(len(recipe_tags), 2)
        
        # Test removing an ingredient
        self.recipeApplication.removeIngredientFromRecipe(recipe, ingredient1)
        updated_ingredients = self.recipeApplication.getRecipeIngredients(recipe)
        self.assertEqual(len(updated_ingredients), 1)
        
        # Test removing a tag
        self.recipeApplication.removeTagFromRecipe(recipe, tag1)
        updated_tags = self.recipeApplication.getRecipeTags(recipe)
        self.assertEqual(len(updated_tags), 1)
        
    def test_user_recipe_relationship(self):
        """Test the relationship between users and their recipes"""
        # Create two users
        self.accountApplication.createAccount('user1', 'password1')
        self.accountApplication.createAccount('user2', 'password2')
        
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        
        # Create recipes for each user
        recipe1 = self.recipeApplication.createRecipe(
            author=user1,
            title='User 1 Recipe',
            description='Recipe by user 1',
            instructions='User 1 instructions',
            duration=15,
            servings=2,
            calories=200
        )
        
        recipe2 = self.recipeApplication.createRecipe(
            author=user2,
            title='User 2 Recipe',
            description='Recipe by user 2',
            instructions='User 2 instructions',
            duration=25,
            servings=4,
            calories=300
        )
        
        # Get recipes for each user
        user1_recipes = self.recipeApplication.getUsersRecipes(user1)
        user2_recipes = self.recipeApplication.getUsersRecipes(user2)
        
        # Verify each user has their own recipe
        self.assertEqual(len(user1_recipes), 1)
        self.assertEqual(len(user2_recipes), 1)
        
        self.assertEqual(user1_recipes[0].title, 'User 1 Recipe')
        self.assertEqual(user2_recipes[0].title, 'User 2 Recipe')
        
        # Verify users don't have access to each other's recipes
        self.assertNotEqual(user1_recipes, user2_recipes)
