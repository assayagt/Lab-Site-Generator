import unittest
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabWebsitesTests.BaseTestClass import BaseTestClass


class TestLogin(BaseTestClass):
    def setUp(self):
        # Call parent setUp to initialize mocks
        super().setUp()
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for multiple users
        self.user_id1 = self.generator_system_service.enter_generator_system().get_data()
        self.user_id2 = self.generator_system_service.enter_generator_system().get_data()
        self.user_id3 = self.generator_system_service.enter_generator_system().get_data()


    def tearDown(self):
        # Call parent tearDown to stop mocks
        super().tearDown()
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