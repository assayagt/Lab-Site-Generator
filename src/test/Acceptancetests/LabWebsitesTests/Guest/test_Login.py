import unittest

from selenium.webdriver.common.devtools.v85.browser import set_window_bounds

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestLoginFunction(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a website for testing login
        self.website_name = "Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.BASIC
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components, self.template)

        # Add lab members and managers
        self.lab_members = {"member1@example.com": "Member One", "member2@example.com": "Member Two"}
        self.lab_managers = {}
        self.site_creator = {"email": "nitzan861999@gmail.com", "full_name": "Site Creator"}
        self.generator_system_service.create_new_lab_website(self.domain, self.lab_members, self.lab_managers, self.site_creator)

        self.user_id_lab_website = self.lab_system_service.enter_lab_website(self.domain).get_data()

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_login(self):
        # Test successful login for an existing lab member
        response = self.lab_system_service.login(self.domain, self.user_id_lab_website, "member1@example.com")
        self.assertTrue(response.is_success())

    def test_login_user_not_exist(self):
        # Test login for a user ID that doesn't exist
        invalid_user_id = "nonexistent_user"
        response = self.lab_system_service.login(self.domain, invalid_user_id, "member1@example.com")
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_EXIST.value)

    def test_login_email_not_member(self):
        # Test login with an email that is not associated with a lab member
        non_member_email = "nonmember@example.com"
        response = self.lab_system_service.login(self.domain, self.user_id_lab_website, non_member_email)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), "Registration request sent to all lab managers.")

    def test_login_email_rejected(self):
        # Simulate lab managers rejecting the registration request
        non_member_email = "nonmember@example.com"
        self.lab_system_service.login(self.domain, self.user_id, non_member_email)

        # Simulate rejection by managers
        for manager_email in self.lab_managers.keys():
            self.lab_system_service.reject_registration_request(self.domain, manager_email, non_member_email)

        # Attempt login again
        response = self.lab_system_service.login(self.domain, self.user_id, non_member_email)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_APPROVED.value)

    def test_login_email_approved(self):
        # Simulate lab managers approving the registration request
        non_member_email = "nonmember@example.com"
        self.lab_system_service.login(self.domain, self.user_id, non_member_email)

        # Simulate approval by managers
        for manager_email in self.lab_managers.keys():
            self.lab_system_service.approve_registration_request(self.domain, manager_email, non_member_email)

        # Attempt login again
        response = self.lab_system_service.login(self.domain, self.user_id, non_member_email)
        self.assertTrue(response.is_success())
        self.assertEqual(response.get_message(), "Login successful.")

    def test_login_invalid_domain(self):
        # Test login with an invalid domain
        invalid_domain = "invalid.example.com"
        response = self.lab_system_service.login(invalid_domain, self.user_id, "member1@example.com")
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

    def test_login_user_not_logged_in(self):
        # Test login when the user is not logged into the generator system
        self.lab_system_service.logout(self.user_id)
        response = self.lab_system_service.login(self.domain, self.user_id, "member1@example.com")
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_LOGGED_IN.value)

