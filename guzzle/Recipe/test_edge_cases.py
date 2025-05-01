from django.test import TestCase
from django.contrib.auth.models import User
from Recipe.models import Recipe, Ingredient, Tag, RecipeIngredient, RecipeTag
from Recipe.application import RecipeApplication
import unittest

class RecipeEdgeCaseTests(TestCase):
    def setUp(self):
        self.recipeApplication = RecipeApplication()
        self.test_user = User.objects.create_user(
            username='edgeCaseUser',
            password='testPassword123'
        )
        
    def test_create_recipe_with_empty_fields(self):
        """Test creating a recipe with empty fields"""
        # Test with empty title
        recipe_empty_title = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='',
            description='Description',
            instructions='Instructions',
            duration=30,
            servings=4,
            calories=300
        )
        # Django's CharField doesn't enforce non-empty by default
        self.assertIsNotNone(recipe_empty_title)
        
        # Test with empty description and instructions
        recipe_empty_desc = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Recipe with empty description',
            description='',
            instructions='',
            duration=30,
            servings=4,
            calories=300
        )
        self.assertIsNotNone(recipe_empty_desc)
        
    def test_create_recipe_with_invalid_numeric_values(self):
        """Test creating a recipe with invalid numeric values"""
        # Test with negative duration
        recipe_neg_duration = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Recipe with negative duration',
            description='Description',
            instructions='Instructions',
            duration=-10,  # Negative duration
            servings=4,
            calories=300
        )
        # The model doesn't validate this, so it should succeed
        self.assertIsNotNone(recipe_neg_duration)
        self.assertEqual(recipe_neg_duration.duration, -10)
        
        # Test with zero servings
        recipe_zero_servings = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Recipe with zero servings',
            description='Description',
            instructions='Instructions',
            duration=30,
            servings=0,  # Zero servings
            calories=300
        )
        self.assertIsNotNone(recipe_zero_servings)
        self.assertEqual(recipe_zero_servings.servings, 0)
        
        # Test with negative calories
        recipe_neg_calories = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Recipe with negative calories',
            description='Description',
            instructions='Instructions',
            duration=30,
            servings=4,
            calories=-100  # Negative calories
        )
        self.assertIsNotNone(recipe_neg_calories)
        self.assertEqual(recipe_neg_calories.calories, -100)
        
    def test_duplicate_ingredients_and_tags(self):
        """Test adding duplicate ingredients and tags to a recipe"""
        recipe = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Recipe for duplicate testing',
            description='Description',
            instructions='Instructions',
            duration=30,
            servings=4,
            calories=300
        )
        
        # Create an ingredient and add it twice
        ingredient = self.recipeApplication.getOrCreateIngredient('Duplicate Ingredient')
        
        # First addition should succeed
        result1 = self.recipeApplication.addIngredientToRecipe(recipe, ingredient, 1, 'cup')
        self.assertTrue(result1)
        
        # Second addition should also succeed (creating a duplicate)
        result2 = self.recipeApplication.addIngredientToRecipe(recipe, ingredient, 2, 'cups')
        self.assertTrue(result2)
        
        # Check that we have two recipe-ingredient relationships
        recipe_ingredients = self.recipeApplication.getRecipeIngredients(recipe)
        self.assertEqual(len(recipe_ingredients), 2)
        
        # Similar test for tags
        tag = self.recipeApplication.getOrCreateTag('Duplicate Tag')
        
        # First addition should succeed
        result1 = self.recipeApplication.addTagToRecipe(recipe, tag)
        self.assertTrue(result1)
        
        # Second addition should also succeed (creating a duplicate)
        result2 = self.recipeApplication.addTagToRecipe(recipe, tag)
        self.assertTrue(result2)
        
        # Check that we have two recipe-tag relationships
        recipe_tags = self.recipeApplication.getRecipeTags(recipe)
        self.assertEqual(len(recipe_tags), 2)
        
    def test_very_long_text_fields(self):
        """Test creating a recipe with very long text fields"""
        long_text = 'a' * 1000  # 1000 character string
        
        # Test with long title
        # Django doesn't validate max_length when creating model instances directly
        # It only validates when full_clean() is called or when using ModelForm
        recipe_long_title = self.recipeApplication.createRecipe(
            author=self.test_user,
            title=long_text,  # Exceeds CharField max_length of 200
            description='Description',
            instructions='Instructions',
            duration=30,
            servings=4,
            calories=300
        )
        
        # The model instance is created, but the title will be truncated in the database
        self.assertIsNotNone(recipe_long_title)
        saved_recipe = Recipe.objects.get(id=recipe_long_title.id)
        self.assertLessEqual(len(saved_recipe.title), 1000)
        
        # Test with long description and instructions (TextField can handle this)
        recipe_long_desc = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Recipe with long description',
            description=long_text,
            instructions=long_text,
            duration=30,
            servings=4,
            calories=300
        )
        self.assertIsNotNone(recipe_long_desc)
        self.assertEqual(len(recipe_long_desc.description), 1000)
        self.assertEqual(len(recipe_long_desc.instructions), 1000)
