import unittest
from unittest.mock import patch

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabWebsitesTests.BaseTestClass import BaseTestClass

class TestLoginFunction(BaseTestClass):
    def setUp(self):
        # Call parent setUp to initialize mocks
        super().setUp()
        
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.site_creator_email = "sagyto@gmail.com"
        self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(None, self.site_creator_email)

        # Create a website for testing login
        self.website_name = "Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.site_creator_email, self.website_name, self.domain, self.components, self.template)

        # Add lab members and managers
        self.lab_members = {"member1@example.com": {"full_name": "Member One", "degree": "B.Sc."}, "member2@example.com": {"full_name":"Member Two", "degree": "M.Sc."}}
        self.lab_managers = {}
        self.site_creator = {"email": self.site_creator_email, "full_name": "Site Creator", "degree": "Ph.D."}
        self.generator_system_service.create_new_lab_website(self.domain, self.lab_members, self.lab_managers, self.site_creator, "")

    def tearDown(self):
        # Call parent tearDown to stop mocks
        super().tearDown()
        self.generator_system_service.reset_system()
        self.lab_system_service.reset_system()

    def test_successful_login(self):
        member_email = "member1@example.com"  # Using email as google token for testing
        response = self.lab_system_service.login(self.domain, None, member_email)
        self.assertTrue(response.is_success())

    def test_login_email_not_member(self):
        non_member_email = "nonmember@example.com"
        response = self.lab_system_service.login(self.domain, None, non_member_email)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_REGISTERED.value)

    def test_login_email_not_member_registration_request_already_sent(self):
        non_member_email = "nonmember@example.com"
        self.lab_system_service.login(self.domain, None, non_member_email)
        response = self.lab_system_service.login(self.domain, None, non_member_email)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.REGISTRATION_EMAIL_ALREADY_SENT_TO_MANAGER.value)

#TODO: Think how to test it
    """
    def test_login_email_rejected(self):
        non_member_email = "nonmember@example.com"
        self.lab_system_service.login(self.domain, None, non_member_email)
        self.lab_system_service.login(self.domain, None, self.site_creator_email)
        self.lab_system_service.reject_registration_request(self.domain, self.site_creator_userId, non_member_email)
        response = self.lab_system_service.login(self.domain, None, non_member_email)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.REGISTRATION_REQUEST_REJECTED_BY_MANAGER.value)

    def test_login_email_approved(self):
        non_member_email = "nonmember@example.com"
        self.lab_system_service.login(self.domain, None, non_member_email)
        self.lab_system_service.login(self.domain, None, self.site_creator_email)
        self.lab_system_service.approve_registration_request(self.domain, self.site_creator_userId, non_member_email, "Non Member", "B.Sc.")
        response = self.lab_system_service.login(self.domain, None, non_member_email)
        self.assertTrue(response.is_success())
"""
    def test_login_invalid_domain(self):
        invalid_domain = "invalid.example.com"
        member_email = "member1@example.com"
        response = self.lab_system_service.login(invalid_domain, None, member_email)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

if __name__ == "__main__":
    unittest.main()


