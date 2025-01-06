import unittest
from http.client import responses

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.Util.Response import Response
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests

class TestRegisterNewLabMemberFromLabWebsite(unittest.TestCase):
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
            self.labMember1_email: {"full_name":self.labMember1_name, "degree": Degree.PHD},
            self.labMember2_email: {"full_name":"Member Two", "degree": Degree.MSC}
        }
        self.nominator_manager_email = "manager1@example.com"
        self.lab_managers = {
            self.nominator_manager_email: {"full_name":"Manager One", "degree": Degree.PHD},
        }

        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.BASIC
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)

        self.generator_system_service.create_new_lab_website(
            self.domain, self.lab_members, self.lab_managers, {"email": self.site_creator_email, "full_name": "Site Creator", "degree": Degree.PHD}
        )

        # Simulate a lab manager login
        self.manager_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.member1_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.manager_userId, self.nominator_manager_email)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_register_new_lab_member_success(self):
        """
        Test that a lab manager can successfully register a new lab member.
        """
        email_to_register = "new_member@example.com"
        full_name = "New Member"
        degree = Degree.BSC
        # Perform the operation
        response = self.lab_system_service.register_new_LabMember_from_labWebsite(
            self.manager_userId, email_to_register, full_name, degree, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the new lab member is added
        lab_members = self.lab_system_service.get_all_lab_members(self.domain).get_data()
        self.assertIn(email_to_register, lab_members)

    def test_register_new_lab_member_failure_user_not_manager(self):
        """
        Test that a non-manager cannot register a new lab member.
        """
        # Simulate a lab member (not manager) login
        self.lab_system_service.login(self.domain, self.member1_userId, self.labMember1_email)

        email_to_register = "new_member@example.com"
        full_name = "New Member"
        degree = Degree.BSC

        # Attempt to perform the operation
        response = self.lab_system_service.register_new_LabMember_from_labWebsite(
            self.member1_userId, email_to_register, full_name, degree, self.domain
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER_OR_CREATOR.value)

    def test_register_new_lab_member_failure_email_already_associated(self):
        """
        Test that attempting to register an email already associated with a member raises an error.
        """
        email_to_register = self.labMember1_email
        full_name = "Duplicated Member"
        degree = Degree.BSC

        # Attempt to perform the operation
        response = self.lab_system_service.register_new_LabMember_from_labWebsite(
            self.manager_userId, email_to_register, full_name, degree, self.domain
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_MEMBER.value)

    def test_register_new_lab_member_failure_user_not_logged_in(self):
        """
        Test that a user who is not logged in cannot register a new lab member.
        """
        # Simulate a logout for the manager
        self.lab_system_service.logout(self.domain, self.manager_userId)

        email_to_register = "new_member@example.com"
        full_name = "New Member"
        degree = Degree.BSC

        # Attempt to perform the operation
        response = self.lab_system_service.register_new_LabMember_from_labWebsite(
            self.manager_userId, email_to_register, full_name, degree, self.domain
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_register_new_lab_member_failure_invalid_email(self):
        """
        Test that an invalid email raises an error during registration.
        """
        email_to_register = "invalid_email"
        full_name = "Invalid Email Member"
        degree = Degree.BSC

        # Attempt to perform the operation
        response = self.lab_system_service.register_new_LabMember_from_labWebsite(
            self.manager_userId, email_to_register, full_name, degree, self.domain
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_EMAIL_FORMAT.value)

    def test_register_new_lab_member_failure_invalid_degree(self):
        """
        Test that an invalid degree raises an error during registration.
        """
        email_to_register = "new_member@example.com"
        full_name = "New Member"
        degree = "Invalid"

        # Attempt to perform the operation
        response = self.lab_system_service.register_new_LabMember_from_labWebsite(
            self.manager_userId, email_to_register, full_name, degree, self.domain
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_DEGREE.value)
