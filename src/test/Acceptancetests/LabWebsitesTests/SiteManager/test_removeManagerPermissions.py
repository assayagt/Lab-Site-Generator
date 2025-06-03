import unittest

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests


class TestRemoveManagerPermission(unittest.TestCase):
    def setUp(self):
        # Initialize the system with real data and components
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="creator@example.com")

        # Create a lab website
        self.domain = "lab1.example.com"
        self.manager1_email = "manager1@example.com"
        self.manager2_email = "manager2@example.com"
        self.lab_creator_email = "creator@example.com"
        self.lab_creator_name = "Creator"
        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)
        self.lab_members = {"member1@example.com": {"full_name": "Member One", "degree": "B.Sc."}}
        self.lab_managers = {
            self.manager1_email: {"full_name": "Manager One", "degree": "M.Sc."},
            self.manager2_email: {"full_name": "Manager Two", "degree": "M.Sc."}
        }
        self.site_creator = {"email": self.lab_creator_email, "full_name": self.lab_creator_name, "degree": "Ph.D."}
        self.creator_scholar_link = "https://scholar.google.com/citations?user=creator"
        response = self.generator_system_service.create_new_lab_website(
            self.domain,
            self.lab_members,
            self.lab_managers,
            self.site_creator,
            self.creator_scholar_link
        )

        # Simulate a lab manager login
        self.manager_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.manager_userId, self.manager1_email)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_remove_manager_permission_success(self):
        """
        Test that a lab manager can successfully remove another manager's permissions.
        """
        response = self.lab_system_service.remove_manager_permission(
            self.manager_userId, self.manager2_email, self.domain
        )
        self.assertTrue(response.is_success())

        # Validate that the manager is now a member
        members = self.lab_system_service.get_all_lab_members(self.domain).get_data()
        self.assertIn(self.manager2_email, members)

        # Validate that the user is no longer in the manager list
        managers = self.lab_system_service.get_all_lab_managers(self.domain).get_data()
        self.assertNotIn(self.manager2_email, managers)

    def test_remove_manager_permission_failure_not_manager(self):
        """
        Test that a user who is not a manager cannot remove permissions from another manager.
        """
        # Simulate a lab member login
        member_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, member_userId, "member1@example.com")

        response = self.lab_system_service.remove_manager_permission(
            member_userId, self.manager2_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER_OR_CREATOR.value)

    def test_remove_manager_permission_failure_creator_permissions(self):
        """
        Test that the permissions of the lab creator cannot be removed.
        """
        response = self.lab_system_service.remove_manager_permission(
            self.manager_userId, self.lab_creator_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def test_remove_manager_permission_failure_manager_not_exist(self):
        """
        Test that an error is raised when trying to remove permissions from a non-existent manager.
        """
        non_existent_email = "nonexistent@example.com"

        response = self.lab_system_service.remove_manager_permission(
            self.manager_userId, non_existent_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def test_remove_manager_permission_failure_user_not_logged_in(self):
        """
        Test that a user who is not logged in cannot remove permissions from a manager.
        """
        # Simulate logout for the manager
        self.lab_system_service.logout(self.domain, self.manager_userId)

        response = self.lab_system_service.remove_manager_permission(
            self.manager_userId, self.manager2_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_remove_manager_permission_failure_user_is_not_manager(self):
        """
        Test that a user who is not a manager cannot have their permissions removed.
        """
        lab_member_email = "member1@example.com"

        response = self.lab_system_service.remove_manager_permission(
            self.manager_userId, lab_member_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)
