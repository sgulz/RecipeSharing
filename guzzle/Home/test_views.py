from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Recipe.models import Recipe
from Recipe.application import RecipeApplication

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.recipeApplication = RecipeApplication()
        
        # Create test user
        self.test_user = User.objects.create_user(
            username='homeViewTestUser',
            password='testPassword123'
        )
        
        # Create some test recipes
        self.recipe1 = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Test Recipe 1',
            description='Description for test recipe 1',
            instructions='Instructions for test recipe 1',
            duration=30,
            servings=4,
            calories=300
        )
        
        self.recipe2 = self.recipeApplication.createRecipe(
            author=self.test_user,
            title='Test Recipe 2',
            description='Description for test recipe 2',
            instructions='Instructions for test recipe 2',
            duration=45,
            servings=6,
            calories=450
        )
        
        # URL for home page
        self.home_url = reverse('home')
        
    def test_home_page_status_code(self):
        """Test that home page returns a 200 status code"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        
    def test_home_page_template(self):
        """Test that home page uses the correct template"""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'homePage.html')
        
    def test_home_page_contains_recipes(self):
        """Test that home page contains the recipes"""
        # Log in the test user
        self.client.force_login(self.test_user)
        
        response = self.client.get(self.home_url)
        
        # Check that the recipes are in the context
        self.assertIn('recipes', response.context)
        recipes = response.context['recipes']
        
        # Check that both test recipes are in the context
        self.assertEqual(len(recipes), 2)
        
        # Check recipe titles are in the HTML response
        self.assertContains(response, 'Test Recipe 1')
        self.assertContains(response, 'Test Recipe 2')
        
    def test_home_page_with_no_recipes(self):
        """Test home page behavior when there are no recipes"""
        # Delete all recipes
        Recipe.objects.all().delete()
        
        response = self.client.get(self.home_url)
        
        # Check that the recipes context is empty
        self.assertIn('recipes', response.context)
        recipes = response.context['recipes']
        self.assertEqual(len(recipes), 0)
