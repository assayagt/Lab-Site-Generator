import unittest

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.test.Acceptancetests.LabWebsitesTests.BaseTestClass import BaseTestClass


class TestSetFullNameByMember(BaseTestClass):
    def setUp(self):
        # Call parent setUp to initialize mocks
        super().setUp()
        # Initialize the system with real data and components
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="manager1@example.com")

        # Create a lab website
        self.domain = "lab1.example.com"
        self.site_creator_email = "creator@example.com"
        self.labMember1_email = "member1@example.com"
        self.labMember1_name = "Member One"
        self.labMember2_email = "member2@example.com"
        self.labMember2_name = "Member Two"
        self.labManager1_email = "manager1@example.com"
        self.labManager1_name = "Manager One"
        self.lab_managers = {
            self.labManager1_email: {"full_name":self.labManager1_name, "degree": "Ph.D."},
        }
        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)
        self.generator_system_service.create_new_lab_website(
            self.domain, {self.labMember1_email: {"full_name":self.labMember1_name, "degree":"M.Sc."}, self.labMember2_email: {"full_name":self.labMember2_name, "degree":"B.Sc."}},
            self.lab_managers,
            {"email": self.site_creator_email, "full_name": "Site Creator", "degree": "Ph.D."},
            ""
        )

        # Simulate a lab member login
        self.labMember1_userId = self.lab_system_service.enter_lab_website(self.domain)
        self.labMember1_userId = self.lab_system_service.login(self.domain, self.labMember1_userId, self.labMember1_email).get_data()
        self.labManager1_userId = self.lab_system_service.enter_lab_website(self.domain)
        self.labManager1_userId = self.lab_system_service.login(self.domain, self.labManager1_userId, self.labManager1_email).get_data()

    def tearDown(self):
        # Call parent tearDown to stop mocks
        super().tearDown()
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_set_fullName_by_member_success(self):
        """
        Test that a lab member can successfully set their full name.
        """
        new_full_name = "Updated Member One"

        # Set the full name
        response = self.lab_system_service.set_fullName_by_member(
            self.labMember1_userId, new_full_name, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the full name was successfully updated
        member_data = self.lab_system_service.get_all_lab_members(self.domain).get_data()
        for member in member_data:
            if member["email"] == self.labMember1_email:
                self.assertEqual(member["fullName"], new_full_name)
                break

    def test_set_fullName_by_member_failure_empty_fullName(self):
        """
        Test that an empty full name cannot be set.
        """
        empty_full_name = ""

        response = self.lab_system_service.set_fullName_by_member(
            self.labMember1_userId, empty_full_name, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_FULL_NAME.value)

    def test_set_fullName_by_alumni_success(self):
        new_full_name = "Name Member"

        self.lab_system_service.define_member_as_alumni(self.labManager1_userId, self.labMember1_email, self.domain)
        # Set the bio
        response = self.lab_system_service.set_fullName_by_member(
            self.labMember1_userId, new_full_name, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the bio was successfully set
        member_data = self.lab_system_service.get_all_alumnis(self.domain).get_data()
        for member in member_data:
            if member["email"] == self.labMember1_email:
                self.assertEqual(member["fullName"], new_full_name)
                break