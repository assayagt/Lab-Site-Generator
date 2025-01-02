import unittest
from src.test.Acceptancetests.ProxyToTests import ProxyToTest
from src.main.Util.Response import Response
from src.main.Util.ExceptionsEnum import ExceptionsEnum


class TestLogout(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for multiple users
        self.user_id1 = self.generator_system_service.enter_generator_system().get_data()
        self.user_id2 = self.generator_system_service.enter_generator_system().get_data()
        self.user_id3 = self.generator_system_service.enter_generator_system().get_data()

        # Log in users
        self.generator_system_service.login(self.user_id1, "user1@example.com")
        self.generator_system_service.login(self.user_id2, "user2@example.com")
        self.generator_system_service.login(self.user_id3, "user3@example.com")

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.logout(self.user_id1)
        self.generator_system_service.logout(self.user_id2)
        self.generator_system_service.logout(self.user_id3)

    def test_successful_logout(self):
        # Test successful logout for all users
        response1 = self.generator_system_service.logout(self.user_id1)
        self.assertTrue(response1.is_success())

        response2 = self.generator_system_service.logout(self.user_id2)
        self.assertTrue(response2.is_success())

        response3 = self.generator_system_service.logout(self.user_id3)
        self.assertTrue(response3.is_success())

    def test_logout_without_login(self):
        # Test logout without login (enter system but no login)
        user_id4 = self.generator_system_service.enter_generator_system().get_data()
        response = self.generator_system_service.logout(user_id4)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_logout_after_already_logged_out(self):
        # Log out a user and attempt to log out again
        self.generator_system_service.logout(self.user_id1)
        response = self.generator_system_service.logout(self.user_id1)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)


