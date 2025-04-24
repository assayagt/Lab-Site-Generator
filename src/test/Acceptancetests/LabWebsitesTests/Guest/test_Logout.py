import unittest

from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestLogoutFunction(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a website for testing logout
        self.website_name = "Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components, self.template)

        # Add lab members and managers
        self.site_creator_email = "someMail@gmail.com"
        self.lab_members = {"member1@example.com": {"full_name": "Member One","degree": "B.Sc."}, "member2@example.com": {"full_name": "Member Two", "degree": "M.Sc."}}
        self.lab_managers = {}
        self.site_creator = {"email": self.site_creator_email, "full_name": "Site Creator", "degree": "Ph.D."}
        self.generator_system_service.create_new_lab_website(self.domain, self.lab_members, self.lab_managers, self.site_creator)

        # Simulate entering the lab website
        self.user_id_lab_website = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.site_creator_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_logout(self):
        # Test successful logout for an active user
        self.lab_system_service.login(self.domain, self.site_creator_userId, self.site_creator_email)
        response = self.lab_system_service.logout(self.domain, self.site_creator_userId)
        self.assertTrue(response.is_success())

    def test_logout_user_not_logged_in(self):
        # Test logout for a user who is not logged in
        response = self.lab_system_service.logout(self.domain, self.site_creator_userId)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_logout_invalid_domain(self):
        # Test logout with an invalid domain
        invalid_domain = "invalid.example.com"
        self.lab_system_service.login(self.domain, self.site_creator_userId, self.site_creator_email)
        response = self.lab_system_service.logout(invalid_domain, self.site_creator_email)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

    def test_logout_multiple_sessions(self):
        # Test logout for a user with multiple sessions
        self.lab_system_service.login(self.domain, self.site_creator_userId, self.site_creator_email)
        self.lab_system_service.login(self.domain, self.user_id_lab_website, "member1@example.com")  # Second session
        response = self.lab_system_service.logout(self.domain, self.user_id_lab_website)
        self.assertTrue(response.is_success())  # Logout should work for any active session
