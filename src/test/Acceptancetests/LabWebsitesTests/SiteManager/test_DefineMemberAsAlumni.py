import unittest

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests


class TestDefineMemberAsAlumni(unittest.TestCase):
    def setUp(self):
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
            self.labManager1_email: {"full_name":self.labManager1_name, "degree": Degree.PHD},
        }
        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.BASIC
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)
        self.generator_system_service.create_new_lab_website(
            self.domain, {self.labMember1_email: {"full_name":self.labMember1_name, "degree":Degree.BSC}, self.labMember2_email: {"full_name":self.labMember2_name, "degree":Degree.BSC}}, self.lab_managers,
            {"email": self.site_creator_email, "full_name": "Site Creator", "degree": Degree.PHD}
        )

        # Simulate a lab manager login
        self.manager_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.siteCreator_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.manager_userId, "manager1@example.com")

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_define_member_as_alumni_success(self):
        """
        Test that a lab manager can successfully define a lab member as alumni.
        """
        response = self.lab_system_service.define_member_as_alumni(
            self.manager_userId, self.labMember1_email, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the member is now in the alumni list
        alumni = self.lab_system_service.get_all_alumnis(self.domain).get_data()
        self.assertIn(self.labMember1_email, alumni)

        # Validate that the member is no longer in the member list
        members = self.lab_system_service.get_all_lab_members(self.domain).get_data()
        self.assertNotIn(self.labMember1_email, members)

    def test_define_manager_as_alumni_success(self):
        """
        Test that a lab manager can successfully define a lab member as alumni.
        """
        self.lab_system_service.login(self.domain, self.siteCreator_userId, self.site_creator_email)
        response = self.lab_system_service.define_member_as_alumni(
            self.siteCreator_userId, self.labManager1_email, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the member is now in the alumni list
        alumni = self.lab_system_service.get_all_alumnis(self.domain).get_data()
        self.assertIn(self.labManager1_email, alumni)

        # Validate that the member is no longer in the member list
        managers = self.lab_system_service.get_all_lab_managers(self.domain).get_data()
        self.assertNotIn(self.labManager1_email, managers)

    def test_define_member_as_alumni_failure_not_manager(self):
        """
        Test that a non-manager user cannot define a member as alumni.
        """
        # Simulate a lab member login
        member_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, member_userId, self.labMember1_email)

        response = self.lab_system_service.define_member_as_alumni(
            member_userId, self.labMember2_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER_OR_CREATOR.value)

    def test_define_member_as_alumni_failure_member_does_not_exist(self):
        """
        Test that an error is raised when trying to define a non-existent member as alumni.
        """
        non_existent_email = "nonexistent@example.com"

        response = self.lab_system_service.define_member_as_alumni(
            self.manager_userId, non_existent_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER.value)

    def test_define_member_as_alumni_failure_site_creator(self):
        """
        Test that the site creator cannot be defined as alumni.
        """
        response = self.lab_system_service.define_member_as_alumni(
            self.manager_userId, self.site_creator_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.SITE_CREATOR_CANT_BE_ALUMNI.value)

    def test_define_member_as_alumni_failure_user_not_logged_in(self):
        """
        Test that a user who is not logged in cannot define a member as alumni.
        """
        # Simulate logout for the manager
        self.lab_system_service.logout(self.domain, self.manager_userId)

        response = self.lab_system_service.define_member_as_alumni(
            self.manager_userId, self.labMember1_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)