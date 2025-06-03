import unittest

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.main.DomainLayer.LabWebsites.User.Degree import Degree

class TestSetDegreeByMember(unittest.TestCase):
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
            self.domain, {self.labMember1_email: {"full_name":self.labMember1_name, "degree": "B.Sc."}, self.labMember2_email: {"full_name":self.labMember2_name, "degree": "M.Sc."}},
            self.lab_managers,
            {"email": self.site_creator_email, "full_name": "Site Creator", "degree": "Ph.D."},
            ""
        )

        # Simulate a lab member login
        self.labMember1_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.labManager1_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.labMember1_userId, self.labMember1_email)
        self.lab_system_service.login(self.domain, self.labManager1_userId, self.labManager1_email)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_set_degree_by_member_success(self):
        """
        Test that a lab member can successfully set their degree.
        """
        new_degree = "Ph.D."

        # Set the degree
        response = self.lab_system_service.set_degree_by_member(
            self.labMember1_userId, new_degree, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the degree was successfully updated
        member_data = self.lab_system_service.get_all_lab_members(self.domain).get_data()
        self.assertEqual(member_data[self.labMember1_email].get_degree(), new_degree)

    def test_set_degree_by_member_failure_not_logged_in(self):
        """
        Test that a member who is not logged in cannot set their degree.
        """
        # Simulate logout for the member
        self.lab_system_service.logout(self.domain, self.labMember1_userId)

        new_degree = "B.Sc."

        response = self.lab_system_service.set_degree_by_member(
            self.labMember1_userId, new_degree, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_set_degree_by_member_failure_user_not_member(self):
        """
        Test that a non-lab member cannot set their degree.
        """
        non_member_user_id = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.generator_system_service.login(non_member_user_id, "nonmember@example.com")

        new_degree = "M.Sc."

        response = self.lab_system_service.set_degree_by_member(
            non_member_user_id, new_degree, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_set_degree_by_member_failure_user_does_not_exist(self):
        """
        Test that trying to set a degree for a non-existent member raises an error.
        """
        new_degree = "B.Sc."

        response = self.lab_system_service.set_degree_by_member(
            "nonexistent_user_id", new_degree, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_NOT_EXIST.value)

    def test_set_degree_by_member_failure_invalid_degree(self):
        """
        Test that setting an invalid degree (e.g., empty string) is not allowed.
        """
        invalid_degree = ""

        response = self.lab_system_service.set_degree_by_member(
            self.labMember1_userId, invalid_degree, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_DEGREE.value)

    def test_set_degree_by_alumni_success(self):
        new_degree = "Ph.D."

        self.lab_system_service.define_member_as_alumni(self.labManager1_userId, self.labMember1_email, self.domain)
        # Set the bio
        response = self.lab_system_service.set_degree_by_member(
            self.labMember1_userId, new_degree, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the bio was successfully set
        member_data = self.lab_system_service.get_all_alumnis(self.domain).get_data()
        self.assertEqual(member_data[self.labMember1_email].get_degree(), new_degree)