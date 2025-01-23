import unittest
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template

class TestChangeWebsiteTemplate(unittest.TestCase):
    def setUp(self):
        # Set up the service with the ProxyToTest
        self.generator_system_service = ProxyToTest("Real")

        # Enter the system and create test data
        self.user_id1 = self.generator_system_service.enter_generator_system().data
        self.generator_system_service.login(self.user_id1, "user1@test.com")
        self.domain = "example.com"
        self.components = ["Contact Us", "About Us"]
        self.generator_system_service.create_website(self.user_id1, "Test Site", self.domain, self.components, Template.template1)

    def tearDown(self):
        # Clean up after each test
        self.generator_system_service.reset_system()

    def test_successful_template_change(self):
        # Test changing the template successfully
        response = self.generator_system_service.change_website_template(self.user_id1, self.domain, Template.ADVANCED)
        self.assertTrue(response.is_success())

    def test_user_does_not_exist(self):
        # Test error when user does not exist
        invalid_user_id = "invalid_user"
        response = self.generator_system_service.change_website_template(invalid_user_id, self.domain, Template.ADVANCED)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_EXIST.value)

    def test_user_not_logged_in(self):
        # Test error when user is not logged in
        self.generator_system_service.logout(self.user_id1)
        response = self.generator_system_service.change_website_template(self.user_id1, self.domain, Template.ADVANCED)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_domain_does_not_exist(self):
        # Test error when the domain does not exist
        invalid_domain = "nonexistent.com"
        response = self.generator_system_service.change_website_template(self.user_id1, invalid_domain, Template.ADVANCED)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)