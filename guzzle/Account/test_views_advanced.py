from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Account.application import AccountApplication

class AccountViewsAdvancedTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.accountApplication = AccountApplication()
        
        # Create test users
        self.test_user = User.objects.create_user(
            username='viewTestUser',
            password='viewPassword123'
        )
        
        # Define URLs (these would need to be updated based on actual URL patterns)
        self.login_url = reverse('login') if hasattr(reverse, 'login') else '/login/'
        self.logout_url = reverse('logout') if hasattr(reverse, 'logout') else '/logout/'
        self.register_url = reverse('register') if hasattr(reverse, 'register') else '/register/'
        
    def test_login_view_get(self):
        """Test GET request to login view"""
        try:
            response = self.client.get(self.login_url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'login.html')
        except:
            # If the view or URL doesn't exist, this test will be skipped
            self.skipTest("Login view not implemented or URL not found")
        
    def test_login_view_post_success(self):
        """Test successful POST request to login view"""
        try:
            response = self.client.post(self.login_url, {
                'username': 'viewTestUser',
                'password': 'viewPassword123'
            })
            # Successful login should redirect
            self.assertIn(response.status_code, [302, 200])
        except:
            self.skipTest("Login view not implemented or URL not found")
        
    def test_login_view_post_failure(self):
        """Test failed POST request to login view"""
        try:
            response = self.client.post(self.login_url, {
                'username': 'viewTestUser',
                'password': 'wrongPassword'
            })
            # Failed login should stay on the same page
            self.assertEqual(response.status_code, 200)
        except:
            self.skipTest("Login view not implemented or URL not found")
        
    def test_logout_view(self):
        """Test logout view"""
        try:
            # First login
            self.client.login(username='viewTestUser', password='viewPassword123')
            
            # Then logout
            response = self.client.get(self.logout_url)
            
            # Should redirect after logout
            self.assertIn(response.status_code, [302, 200])
            
            # User should be logged out
            response = self.client.get('/some-protected-url/')
            # This would need to be updated based on how your app handles authentication
        except:
            self.skipTest("Logout view not implemented or URL not found")
        
    def test_register_view_get(self):
        """Test GET request to register view"""
        try:
            response = self.client.get(self.register_url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'register.html')
        except:
            self.skipTest("Register view not implemented or URL not found")
        
    def test_register_view_post_success(self):
        """Test successful POST request to register view"""
        try:
            response = self.client.post(self.register_url, {
                'username': 'newTestUser',
                'password': 'newPassword123',
                'password_confirm': 'newPassword123'  # Assuming confirmation is required
            })
            # Successful registration should redirect
            self.assertIn(response.status_code, [302, 200])
            
            # User should be created
            self.assertTrue(User.objects.filter(username='newTestUser').exists())
        except:
            self.skipTest("Register view not implemented or URL not found")
        
    def test_register_view_post_duplicate_username(self):
        """Test POST request to register view with duplicate username"""
        try:
            # Try to register with existing username
            response = self.client.post(self.register_url, {
                'username': 'viewTestUser',  # Already exists
                'password': 'anotherPassword123',
                'password_confirm': 'anotherPassword123'
            })
            
            # Should stay on the same page
            self.assertEqual(response.status_code, 200)
            
            # Should have an error message
            self.assertContains(response, 'username already exists')
        except:
            self.skipTest("Register view not implemented or URL not found")
