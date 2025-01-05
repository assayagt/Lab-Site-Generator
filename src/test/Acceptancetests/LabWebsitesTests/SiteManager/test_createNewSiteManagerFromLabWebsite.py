import unittest
from http.client import responses

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.Util.Response import Response
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests


class TestCreateNewSiteManagerFromLabWebsite(unittest.TestCase):
    def setUp(self):
        # Initialize the system with real data and components
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a lab website
        self.domain = "lab1.example.com"
        self.site_creator_email = "creator@example.com"
        self.labMember1_email = "member1@example.com"
        self.labMember1_name = "Member One"
        self.labMember2_email = "member2@example.com"
        self.lab_members = {
            self.labMember1_email: self.labMember1_name,
            self.labMember2_email: "Member Two"
        }
        self.nominator_manager_email ="manager1@example.com"
        self.lab_managers = {
            self.nominator_manager_email: "Manager One",
        }

        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.BASIC
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)

        self.generator_system_service.create_new_lab_website(
            self.domain, self.lab_members, self.lab_managers, {"email": self.site_creator_email, "full_name": "Site Creator"}
        )

        # Simulate a lab manager login
        self.nominator_manager_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.nominator_manager_userId, self.nominator_manager_email)
        self.member1_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_create_new_site_manager_success(self):
        """
        Test that a lab manager can successfully nominate a lab member as a new site manager.
        """

        # Perform the operation
        response = self.lab_system_service.create_new_site_manager_from_labWebsite(
            self.nominator_manager_userId, self.domain, self.labMember1_email
        )
        self.assertTrue(response.is_success())

        # Validate that the nominated user is now a manager
        lab_managers = self.lab_system_service.get_all_lab_managers(self.domain).get_data()
        self.assertIn(self.labMember1_email, lab_managers)

        # Validate that the user is no longer listed as a lab member
        lab_members = self.lab_system_service.get_all_lab_members(self.domain).get_data()
        self.assertNotIn(self.labMember1_email, lab_members)

    def test_create_new_site_manager_failure_user_not_manager(self):
        """
        Test that a non-manager cannot nominate a lab member as a site manager.
        """
        # Simulate a lab member (not manager) login
        self.lab_system_service.login(self.domain, self.member1_userId, self.labMember1_email)

        # Attempt to perform the operation
        response = self.lab_system_service.create_new_site_manager_from_labWebsite(self.member1_userId, self.domain, self.labMember2_email)

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER_OR_CREATOR.value)

    def test_create_new_site_manager_failure_lab_member_not_exist(self):
        """
        Test that nominating a user who is not a lab member raises an error.
        """
        nominated_manager_email = "non_existent_member@example.com"

        # Attempt to perform the operation
        response = self.lab_system_service.create_new_site_manager_from_labWebsite(
            self.nominator_manager_userId, self.domain, nominated_manager_email
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)

    def test_create_new_site_manager_failure_user_not_logged_in(self):
        """
        Test that a user who is not logged in cannot nominate a lab member as a site manager.
        """
        # Simulate a logout for the nominating manager
        self.lab_system_service.logout(self.domain, self.nominator_manager_userId)

        # Attempt to perform the operation
        response = self.lab_system_service.create_new_site_manager_from_labWebsite(
            self.nominator_manager_userId, self.domain, self.labMember1_email
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

