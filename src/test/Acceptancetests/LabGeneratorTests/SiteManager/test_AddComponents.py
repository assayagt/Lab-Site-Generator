import unittest
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template

class TestAddComponentsToSite(unittest.TestCase):
    def setUp(self):
        # Set up the service with the ProxyToTest
        self.generator_system_service = ProxyToTest("Real")

        # Enter the system and create test data
        self.user_id1 = self.generator_system_service.enter_generator_system().data
        self.generator_system_service.login(self.user_id1, "manager@test.com")
        self.domain = "example.com"
        self.generator_system_service.create_website(
            self.user_id1, "Test Site", self.domain, ["Homepage", "About Us"], Template.BASIC
        )

    def tearDown(self):
        # Clean up after each test
        self.generator_system_service.reset_system()

    def test_successful_add_components(self):
        # Test adding valid components successfully
        components = ["Contact Us", "Participants"]
        response = self.generator_system_service.add_components_to_site(self.user_id1, self.domain, components)
        self.assertTrue(response.is_success())

    def test_user_does_not_exist(self):
        # Test error when user does not exist
        invalid_user_id = "invalid_user"
        components = ["Participants"]
        response = self.generator_system_service.add_components_to_site(invalid_user_id, self.domain, components)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_EXIST.value)

    def test_user_not_logged_in(self):
        # Test error when user is not logged in
        self.generator_system_service.logout(self.user_id1)
        components = ["Participants"]
        response = self.generator_system_service.add_components_to_site(self.user_id1, self.domain, components)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_user_is_not_site_manager(self):
        # Test error when user is not a site manager
        self.generator_system_service.logout(self.user_id1)
        self.user_id2 = self.generator_system_service.enter_generator_system().data
        self.generator_system_service.login(self.user_id2, "user2@test.com")
        components = ["Media"]
        response = self.generator_system_service.add_components_to_site(self.user_id2, self.domain, components)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def test_domain_does_not_exist(self):
        # Test error when the domain does not exist
        invalid_domain = "nonexistent.com"
        components = ["News"]
        response = self.generator_system_service.add_components_to_site(self.user_id1, invalid_domain, components)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

    def test_invalid_components_format(self):
        # Test error when components are not in a valid format
        invalid_components = "News"  # Not a list
        response = self.generator_system_service.add_components_to_site(self.user_id1, self.domain, invalid_components)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_COMPONENTS_FORMAT.value)

        invalid_components = [123, "News"]  # Mixed types
        response = self.generator_system_service.add_components_to_site(self.user_id1, self.domain, invalid_components)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_COMPONENTS_FORMAT.value)
