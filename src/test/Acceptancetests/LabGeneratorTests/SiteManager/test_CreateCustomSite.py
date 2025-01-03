import unittest
from src.test.Acceptancetests.ProxyToTests import ProxyToTest
from src.main.Util.Response import Response
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestCreateWebsite(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_website_creation(self):
        # Test creating a website successfully
        website_name = "My Lab Website"
        domain = "lab1.example.com"
        components = ["Homepage", "Contact Us", "Research"]
        template = Template.BASIC
        response = self.generator_system_service.create_website(self.user_id, website_name, domain, components, template)
        self.assertTrue(response.is_success())

    def test_user_not_logged_in(self):
        # Test creating a website when the user is not logged in
        website_name = "My Lab Website2"
        domain = "lab2.example.com"
        components = ["Homepage", "Contact Us", "Research"]
        template = Template.BASIC
        self.generator_system_service.logout(self.user_id)
        response = self.generator_system_service.create_website(self.user_id, website_name, domain, components, template)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_user_not_exist(self):
        # Test creating a website with a non-existent user
        website_name = "My Lab Website3"
        domain = "lab3.example.com"
        invalid_user_id = "non_existent_user"
        components = ["Homepage", "Contact Us", "Research"]
        template = Template.BASIC
        response = self.generator_system_service.create_website(invalid_user_id, website_name, domain, components, template)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_EXIST.value)

    def test_duplicate_website_domain(self):
        # Test creating a website with a duplicate domain
        website_name = "My Lab Website4"
        domain = "lab4.example.com"
        components = ["Homepage", "Contact Us", "Research"]
        template = Template.BASIC
        self.generator_system_service.create_website(self.user_id, website_name, domain, components, template)
        response = self.generator_system_service.create_website(self.user_id, "Another Lab Website", domain, components, template)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_ALREADY_EXIST.value)

    def test_invalid_template(self):
        # Test creating a website with an invalid template
        website_name = "My Lab Website5"
        domain = "lab5.example.com"
        invalid_template = "NonExistentTemplate"  # Still testing raw strings as invalid cases
        components = ["Homepage", "Contact Us", "Research"]
        response = self.generator_system_service.create_website(self.user_id, website_name, domain, components, invalid_template)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_TEMPLATE.value)

    def test_missing_website_name(self):
        # Test creating a website with a missing name
        website_name = ""
        domain = "lab6.example.com6"
        components = ["Homepage", "Contact Us", "Research"]
        template = Template.BASIC
        response = self.generator_system_service.create_website(self.user_id, website_name, domain, components, template)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_SITE_NAME.value)

    def test_missing_domain(self):
        # Test creating a website with a missing domain
        website_name = "My Lab Website7"
        domain = ""
        components = ["Homepage", "Contact Us", "Research"]
        template = Template.BASIC
        response = self.generator_system_service.create_website(self.user_id, website_name, domain, components, template)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)
