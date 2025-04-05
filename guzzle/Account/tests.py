from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Account.application import AccountApplication
from django.core.exceptions import ValidationError

class AccountTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.testCredentials = {
            'username': 'tUsername',
            'password': 'tPassword'
        }
        self.accountApplication = AccountApplication()

    def testCreateAccount(self):
        # Tests if accounts are created and added to User table
        self.accountApplication.createAccount(self.testCredentials['username'], self.testCredentials['password'])
        self.assertTrue(User.objects.filter(username=self.testCredentials['username']).exists())

    def testLogin(self):
        # Tests if accounts can be logged in
        self.accountApplication.createAccount(self.testCredentials['username'], self.testCredentials['password'])
        self.assertTrue(self.client.login(username=self.testCredentials['username'], password=self.testCredentials['password']))

    def testCreateAccountWithDuplicateUsername(self):
        # Tests if accounts with duplicate usernames are stopped from being created
        self.accountApplication.createAccount(self.testCredentials['username'], self.testCredentials['password'])
        self.assertFalse(self.accountApplication.createAccount(self.testCredentials['username'], self.testCredentials['password']))

    def testGetCredentials(self):
        # Tests if the getUsername and checkPassword methods work
        self.accountApplication.createAccount(self.testCredentials['username'], self.testCredentials['password'])
        user = User.objects.get(username=self.testCredentials['username'])
        self.client.login(username=self.testCredentials['username'], password=self.testCredentials['password'])
        self.assertEqual(self.accountApplication.getUsername(user), self.testCredentials['username'])
        self.assertTrue(self.accountApplication.checkPassword(self.testCredentials['password'], user))

    def testDeleteAccount(self):
        # Tests if the deleted accounts are removed from the Users table
        self.accountApplication.createAccount(self.testCredentials['username'], self.testCredentials['password'])
        self.assertTrue(User.objects.filter(username=self.testCredentials['username']).exists())  # Confirms the account is in the table
        user = User.objects.get(username=self.testCredentials['username'])
        self.accountApplication.deleteAccount(user)
        self.assertFalse(User.objects.filter(username=self.testCredentials['username']).exists())  # Confirms the account is remove from Users