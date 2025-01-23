import unittest
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestChangeWebsiteDomain(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a website to test domain changes
        self.website_name = "My Lab Website"
        self.original_domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_domain_change(self):
        # Test changing the website domain successfully
        self.generator_system_service.create_website(self.user_id, self.website_name, self.original_domain, self.components, self.template)
        new_domain = "newlab.example.com"
        response = self.generator_system_service.change_website_domain(self.user_id, new_domain, self.original_domain)
        self.assertTrue(response.is_success())
        self.assertEqual(response.get_data(), new_domain)

    def test_website_not_exist(self):
        # Test trying to change the domain of a website that does not exist
        new_domain = "domain.example.com"
        domain = "nonexistent.example.com"
        response = self.generator_system_service.change_website_domain(self.user_id, new_domain, domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

    def test_user_not_logged_in(self):
        # Test changing the domain when the user is not logged in
        self.generator_system_service.create_website(self.user_id, self.website_name, self.original_domain, self.components, self.template)
        new_domain = "newdomain.example.com"
        self.generator_system_service.logout(self.user_id)
        response = self.generator_system_service.change_website_domain(self.user_id, new_domain, self.original_domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_invalid_new_domain_format(self):
        # Test changing the domain to an invalid format
        self.generator_system_service.create_website(self.user_id, self.website_name, self.original_domain, self.components, self.template)
        invalid_domain = "invalid_domain"  # Missing proper domain format
        response = self.generator_system_service.change_website_domain(self.user_id, invalid_domain, self.original_domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)

    def test_user_not_exist(self):
        # Test changing the domain with a non-existent user
        self.generator_system_service.create_website(self.user_id, self.website_name, self.original_domain, self.components, self.template)
        new_domain = "newlab.example.com"
        invalid_user_id = "non_existent_user"
        response = self.generator_system_service.change_website_domain(invalid_user_id, new_domain, self.original_domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_EXIST.value)

    def test_duplicate_domain(self):
        # Test trying to change the domain to an already existing one
        self.generator_system_service.create_website(self.user_id, self.website_name, self.original_domain, self.components, self.template)
        existing_domain = "lab2.example.com"
        self.generator_system_service.create_website(
            self.user_id, "Another Lab Website", existing_domain, self.components, self.template
        )
        response = self.generator_system_service.change_website_domain(self.user_id, existing_domain, self.original_domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_ALREADY_EXIST.value)


