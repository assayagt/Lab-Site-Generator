import unittest
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestChangeSiteLogoByManager(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a website to test logo changing
        self.domain = "lab1.example.com"
        self.website_name = "My Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components, self.template)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_logo_change(self):
        # Test changing the site logo successfully
        response = self.generator_system_service.change_site_logo_by_manager(self.user_id, self.domain)
        self.assertTrue(response.is_success())

    def test_website_not_exist(self):
        # Test changing the logo of a non-existent website
        invalid_domain = "non_existent_domain.example.com"
        response = self.generator_system_service.change_site_logo_by_manager(self.user_id, invalid_domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

    def test_user_not_logged_in(self):
        # Test changing the logo when the user is not logged in
        self.generator_system_service.logout(self.user_id)
        response = self.generator_system_service.change_site_logo_by_manager(self.user_id, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_user_not_manager(self):
        # Test changing the logo by a user who is not the site manager
        other_user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=other_user_id, email="user_2@example.com")
        response = self.generator_system_service.change_site_logo_by_manager(other_user_id, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def test_user_not_exist(self):
        # Test changing the logo with a non-existent user
        invalid_user_id = "non_existent_user"
        response = self.generator_system_service.change_site_logo_by_manager(invalid_user_id, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_EXIST.value)
