from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Account.application import AccountApplication

class AccountSecurityTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.accountApplication = AccountApplication()
        self.testCredentials = {
            'username': 'securityTestUser',
            'password': 'securePassword123'
        }
        # Create a test user for security tests
        self.accountApplication.createAccount(
            self.testCredentials['username'], 
            self.testCredentials['password']
        )
        
    def test_password_validation(self):
        """Test that password validation works correctly"""
        user = User.objects.get(username=self.testCredentials['username'])
        
        # Test with correct password
        self.assertTrue(self.accountApplication.checkPassword(self.testCredentials['password'], user))
        
        # Test with incorrect password
        self.assertFalse(self.accountApplication.checkPassword('wrongPassword', user))
        
    def test_duplicate_username_prevention(self):
        """Test that duplicate usernames are prevented"""
        # Try to create an account with the same username
        result = self.accountApplication.createAccount(
            self.testCredentials['username'],
            'differentPassword123'
        )
        self.assertFalse(result)
        
        # Verify only one user with this username exists
        # This will work now because we're using TransactionTestCase
        matching_users = User.objects.filter(username=self.testCredentials['username']).count()
        self.assertEqual(matching_users, 1)
        
    def test_username_case_sensitivity(self):
        """Test username case sensitivity behavior"""
        # Try to create an account with the same username but different case
        uppercase_username = self.testCredentials['username'].upper()
        
        # Django's default User model treats usernames as case-sensitive
        # This test verifies the expected behavior
        result = self.accountApplication.createAccount(
            uppercase_username,
            'anotherPassword123'
        )
        
        # Check if the account was created (Django's default behaviour allows this)
        self.assertTrue(result)
        self.assertTrue(User.objects.filter(username=uppercase_username).exists())
