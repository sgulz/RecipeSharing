from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from Account.application import AccountApplication

class AccountIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.accountApplication = AccountApplication()
        self.testCredentials = {
            'username': 'testIntegrationUser',
            'password': 'testPassword123'
        }
        # Create a test user for integration tests
        self.accountApplication.createAccount(
            self.testCredentials['username'], 
            self.testCredentials['password']
        )
        
    def add_session_to_request(self, request):
        """Helper method to add session to request"""
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        
    def test_login_logout_flow(self):
        """Test the complete login and logout flow"""
        # Create a request object
        request = self.factory.get('/')
        self.add_session_to_request(request)
        
        # First ensure we can login
        login_successful = self.accountApplication.login(
            request,
            self.testCredentials['username'],
            self.testCredentials['password']
        )
        self.assertTrue(login_successful)
        
        # Set the user as authenticated for logout test
        user = User.objects.get(username=self.testCredentials['username'])
        request.user = user
        
        # Now test logout
        logout_successful = self.accountApplication.logout(request)
        self.assertTrue(logout_successful)
        
    def test_account_creation_and_deletion(self):
        """Test creating and then deleting an account"""
        # Create a new test user
        new_user_credentials = {
            'username': 'deleteTestUser',
            'password': 'deletePassword123'
        }
        
        # Create the account
        creation_successful = self.accountApplication.createAccount(
            new_user_credentials['username'],
            new_user_credentials['password']
        )
        self.assertTrue(creation_successful)
        self.assertTrue(User.objects.filter(username=new_user_credentials['username']).exists())
        
        # Delete the account
        user = User.objects.get(username=new_user_credentials['username'])
        self.accountApplication.deleteAccount(user)
        
        # Verify the account is deleted
        self.assertFalse(User.objects.filter(username=new_user_credentials['username']).exists())
        
    def test_invalid_login_attempt(self):
        """Test that invalid login credentials are rejected"""
        # Create a request object
        request = self.factory.get('/')
        self.add_session_to_request(request)
        
        login_result = self.accountApplication.login(
            request,
            self.testCredentials['username'],
            'wrongPassword'
        )
        self.assertFalse(login_result)
