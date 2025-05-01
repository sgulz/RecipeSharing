from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from Account.application import AccountApplication

class AccountUnitAdvancedTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.accountApplication = AccountApplication()
        self.testCredentials = {
            'username': 'advancedTestUser',
            'password': 'advancedPassword123'
        }
        
        # Create a test user
        self.user = User.objects.create_user(
            username=self.testCredentials['username'],
            password=self.testCredentials['password']
        )
        
    def add_session_to_request(self, request):
        """Helper method to add session to request"""
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        
    def test_login_with_request_object(self):
        """Test login functionality with a request object"""
        request = self.factory.get('/')
        self.add_session_to_request(request)
        request.user = AnonymousUser()
        
        # Test login with correct credentials
        login_result = self.accountApplication.login(
            request,
            self.testCredentials['username'],
            self.testCredentials['password']
        )
        self.assertTrue(login_result)
        
    def test_logout_with_request_object(self):
        """Test logout functionality with a request object"""
        request = self.factory.get('/')
        self.add_session_to_request(request)
        request.user = self.user
        
        # Test logout
        logout_result = self.accountApplication.logout(request)
        self.assertTrue(logout_result)
        
    def test_logout_when_not_logged_in(self):
        """Test logout when not logged in"""
        request = self.factory.get('/')
        self.add_session_to_request(request)
        request.user = AnonymousUser()
        
        # Test logout when not logged in
        logout_result = self.accountApplication.logout(request)
        self.assertIsNone(logout_result)
        
    def test_get_username_with_no_user(self):
        """Test getUsername method with no user provided"""
        # This should raise TypeError because User.get_username() is an instance method
        with self.assertRaises(TypeError):
            self.accountApplication.getUsername()
                
    def test_check_password_with_no_user(self):
        """Test checkPassword method with no user provided"""
        # This should raise TypeError because User.check_password() needs a self argument
        with self.assertRaises(TypeError):
            self.accountApplication.checkPassword('somepassword')
                
    def test_delete_account_with_no_user(self):
        """Test deleteAccount method with no user provided"""
        # This should raise TypeError because User.delete() is an instance method
        with self.assertRaises(TypeError):
            self.accountApplication.deleteAccount()
            
    def test_user_id_management(self):
        """Test getUserID and setUserID methods"""
        # Initially userID should be None
        self.assertIsNone(self.accountApplication.getUserID())
        
        # Set userID
        test_id = 123
        self.accountApplication.setUserID(test_id)
        
        # Check if userID was set correctly
        self.assertEqual(self.accountApplication.getUserID(), test_id)
