import unittest
from src.test.Acceptancetests.ProxyToTests import ProxyToTest
from src.main.Util.Response import Response
from src.main.Util.ExceptionsEnum import ExceptionsEnum


class TestLogin(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for multiple users
        self.user_id1 = self.generator_system_service.enter_generator_system().get_data()
        self.user_id2 = self.generator_system_service.enter_generator_system().get_data()
        self.user_id3 = self.generator_system_service.enter_generator_system().get_data()


    def tearDown(self):
        # Log out users and reset the system after each test
        self.generator_system_service.logout(self.user_id1)
        self.generator_system_service.logout(self.user_id2)
        self.generator_system_service.logout(self.user_id3)

    def test_successful_login(self):
        # Test successful logins
        response1 = self.generator_system_service.login(self.user_id1, "user1@example.com")
        self.assertTrue(response1.is_success())

        response2 = self.generator_system_service.login(self.user_id2, "user2@example.com")
        self.assertTrue(response2.is_success())

        response3 = self.generator_system_service.login(self.user_id3, "user3@example.com")
        self.assertTrue(response3.is_success())

    def test_incorrect_email(self):
        # Test login with incorrect email
        response1 = self.generator_system_service.login(self.user_id1, "wrongemail@example.com")
        self.assertFalse(response1.is_success())
        self.assertEqual(response1.description, ExceptionsEnum.usernameOrPasswordIncorrect.value)

    def test_already_logged_in(self):
        # Log in users
        self.generator_system_service.login(self.user_id1, "user1@example.com")
        self.generator_system_service.login(self.user_id2, "user2@example.com")
        self.generator_system_service.login(self.user_id3, "user3@example.com")

        # Attempt to log in again
        response1 = self.generator_system_service.login(self.user_id1, "user1@example.com")
        self.assertFalse(response1.is_success())
        self.assertEqual(response1.description, ExceptionsEnum.userAlreadyLoggedIn.value)

        response2 = self.generator_system_service.login(self.user_id2, "user2@example.com")
        self.assertFalse(response2.is_success())
        self.assertEqual(response2.description, ExceptionsEnum.userAlreadyLoggedIn.value)

        response3 = self.generator_system_service.login(self.user_id3, "user3@example.com")
        self.assertFalse(response3.is_success())
        self.assertEqual(response3.description, ExceptionsEnum.userAlreadyLoggedIn.value)