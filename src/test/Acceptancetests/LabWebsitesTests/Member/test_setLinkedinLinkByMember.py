import unittest

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.test.Acceptancetests.LabWebsitesTests.BaseTestClass import BaseTestClass


class TestSetLinkedinLinkByMember(BaseTestClass):
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
            self.labManager1_email: {"full_name": self.labManager1_name, "degree":"Ph.D."},
        }
        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)
        self.creator_scholar_link = "https://scholar.google.com/citations?user=creator"
        self.generator_system_service.create_new_lab_website(
            self.domain, {self.labMember1_email: {"full_name":self.labMember1_name, "degree": "B.Sc."}, self.labMember2_email: {"full_name":self.labMember2_name, "degree": "M.Sc."}},
            self.lab_managers,
            {"email": self.site_creator_email, "full_name": "Site Creator", "degree": "Ph.D."},
            self.creator_scholar_link
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

    def test_set_linkedin_link_by_member_success(self):
        """
        Test that a lab member can successfully set a LinkedIn link.
        """
        linkedin_link = "https://www.linkedin.com/in/member1"

        # Set the LinkedIn link
        response = self.lab_system_service.set_linkedin_link_by_member(
            self.labMember1_userId, linkedin_link, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the LinkedIn link was successfully set
        member_data = self.lab_system_service.get_all_lab_members(self.domain).get_data()
        for member in member_data:
            if member["email"] == self.labMember1_email:
                self.assertEqual(member["linkedin_link"], linkedin_link)
                break

    def test_set_linkedin_link_by_member_failure_invalid_linkedin_link(self):
        """
        Test that an invalid LinkedIn link cannot be set.
        """
        invalid_linkedin_link = "invalid-linkedin-link"

        response = self.lab_system_service.set_linkedin_link_by_member(
            self.labMember1_userId, invalid_linkedin_link, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_LINKEDIN_LINK.value)

    def test_set_fullName_by_alumni_success(self):
        linkedin_link = "https://www.linkedin.com/in/member1"

        self.lab_system_service.define_member_as_alumni(self.labManager1_userId, self.labMember1_email, self.domain)
        # Set the linkedin link
        response = self.lab_system_service.set_linkedin_link_by_member(
            self.labMember1_userId, linkedin_link, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the bio was successfully set
        member_data = self.lab_system_service.get_all_alumnis(self.domain).get_data()
        for member in member_data:
            if member["email"] == self.labMember1_email:
                self.assertEqual(member["linkedin_link"], linkedin_link)
                break