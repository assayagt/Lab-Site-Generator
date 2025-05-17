import unittest
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests

class TestRemoveAlumniFromLabWebsite(unittest.TestCase):
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
            self.labManager1_email: {"full_name":self.labManager1_name, "degree": "Ph.D."},
        }
        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)
        self.generator_system_service.create_new_lab_website(
            self.domain, {self.labMember1_email: {"full_name":self.labMember1_name, "degree":"B.Sc."}, self.labMember2_email: {"full_name":self.labMember2_name, "degree":"B.Sc."}}, self.lab_managers,
            {"email": self.site_creator_email, "full_name": "Site Creator", "degree": "Ph.D."}
        )

        # Simulate a lab manager login
        self.manager_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.siteCreator_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.manager_userId, "manager1@example.com")

        # First make a member an alumni
        self.lab_system_service.define_member_as_alumni(self.manager_userId, self.labMember1_email, self.domain)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_remove_alumni_success(self):
        """
        Test that a lab manager can successfully remove an alumni and revert them to a lab member.
        """
        response = self.lab_system_service.remove_alumni_from_labWebsite(
            self.manager_userId, self.labMember1_email, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the member is no longer in the alumni list
        alumni = self.lab_system_service.get_all_alumnis(self.domain).get_data()
        self.assertNotIn(self.labMember1_email, alumni)

        # Validate that the member is back in the member list
        members = self.lab_system_service.get_all_lab_members(self.domain).get_data()
        self.assertIn(self.labMember1_email, members)

    def test_remove_alumni_failure_not_manager(self):
        """
        Test that a non-manager user cannot remove an alumni.
        """
        # Simulate a lab member login
        member_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, member_userId, self.labMember2_email)

        response = self.lab_system_service.remove_alumni_from_labWebsite(
            member_userId, self.labMember1_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER_OR_CREATOR.value)

    def test_remove_alumni_failure_not_alumni(self):
        """
        Test that trying to remove a non-alumni member raises an error.
        """
        response = self.lab_system_service.remove_alumni_from_labWebsite(
            self.manager_userId, self.labMember2_email, self.domain
        )
        self.assertFalse(response.is_success())
        print(response.get_message())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_AN_ALUMNI.value)

    def test_remove_alumni_failure_user_not_logged_in(self):
        """
        Test that a user who is not logged in cannot remove an alumni.
        """
        # Simulate logout for the manager
        self.lab_system_service.logout(self.domain, self.manager_userId)

        response = self.lab_system_service.remove_alumni_from_labWebsite(
            self.manager_userId, self.labMember1_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)
