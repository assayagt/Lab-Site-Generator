import unittest
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestChangeWebsiteName(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a website to test name changing
        self.website_name = "My Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.BASIC
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components, self.template)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_name_change(self):
        # Test changing the website name successfully
        new_name = "My Updated Lab Website"
        response = self.generator_system_service.change_website_name(self.user_id, new_name, self.domain)
        self.assertTrue(response.is_success())
        self.assertEqual(response.get_data(), new_name)

    def test_website_not_exist(self):
        # Test trying to change the name of a website that does not exist
        new_name = "New Lab Website"
        invalid_domain = "non_existent_domain.example.com"
        response = self.generator_system_service.change_website_name(self.user_id, new_name, invalid_domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

    def test_user_not_logged_in(self):
        # Test changing the website name when the user is not logged in
        new_name = "New Lab Website"
        self.generator_system_service.logout(self.user_id)
        response = self.generator_system_service.change_website_name(self.user_id, new_name, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_invalid_new_name(self):
        # Test changing the website name to an invalid name (empty string)
        new_name = ""
        response = self.generator_system_service.change_website_name(self.user_id, new_name, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_SITE_NAME.value)

    def test_user_not_exist(self):
        # Test changing the website name with a non-existent user
        new_name = "Another Lab Website"
        invalid_user_id = "non_existent_user"
        response = self.generator_system_service.change_website_name(invalid_user_id, new_name, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_EXIST.value)
