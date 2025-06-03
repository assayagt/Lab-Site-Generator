import unittest

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum


class TestRemoveSiteManagerFromGenerator(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")
        
        # Reset system before each test to ensure clean state
        self.generator_system_service.reset_system()

        # Simulate entering the generator system for a user
        self.nominator_manager_userId = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.nominator_manager_userId, email="creator@example.com")

        # Create a website and assign a manager
        self.website_name = "My Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.generator_system_service.create_website(self.nominator_manager_userId, self.website_name, self.domain,
                                                     self.components, Template.template1)

        # Add a second manager
        self.manager_toRemove_email = "manager_2@example.com"
        self.manager_toRemove_userId = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.manager_toRemove_userId, email=self.manager_toRemove_email)

        self.lab_members = {"member1@example.com": {"full_name": "Member One", "degree": "B.Sc."},
                            "member2@example.com": {"full_name": "Member Two", "degree": "M.Sc."}}
        self.lab_managers = {self.manager_toRemove_email: {"full_name": "Manager One", "degree": "Ph.D."}}
        self.site_creator = {"email": "creator@example.com", "full_name": "Liron David", "degree": "Ph.D."}
        self.creator_scholar_link = "https://scholar.google.com/citations?user=rgUqRpYAAAAJ&hl=en"

        self.generator_system_service.create_new_lab_website(self.domain, self.lab_members, self.lab_managers, self.site_creator, self.creator_scholar_link)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_removal(self):
        # Test successfully removing a manager
        response = self.generator_system_service.remove_site_manager_from_generator(self.nominator_manager_userId, self.manager_toRemove_email, self.domain)
        self.assertTrue(response.is_success())

    def test_nominator_user_not_logged_in(self):
        # Test removing a manager when the nominator manager is not logged in
        self.generator_system_service.logout(self.nominator_manager_userId)
        response = self.generator_system_service.remove_site_manager_from_generator(
            self.nominator_manager_userId, self.manager_toRemove_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_manager_to_remove_not_exist(self):
        # Test removing a manager who does not exist
        invalid_email = "non_existent_manager@example.com"
        response = self.generator_system_service.remove_site_manager_from_generator(
            self.nominator_manager_userId, invalid_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def test_nominator_user_not_manager(self):
        # Test removing a manager by a user who is not a site manager
        other_userId = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=other_userId, email="non_manager@example.com")
        response = self.generator_system_service.remove_site_manager_from_generator(
            other_userId, self.manager_toRemove_email, self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def test_creator_permissions_cannot_be_removed(self):
        # Test that the permissions of the creator cannot be removed
        response = self.generator_system_service.remove_site_manager_from_generator(
            self.nominator_manager_userId, self.site_creator["email"], self.domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.PERMISSIONS_OF_SITE_CREATOR_CANNOT_BE_REMOVED.value)

    def test_manager_not_associated_with_domain(self):
        # Test removing a manager who is not associated with the domain
        invalid_domain = "other_domain.example.com"
        response = self.generator_system_service.remove_site_manager_from_generator(
            self.nominator_manager_userId, self.manager_toRemove_email, invalid_domain
        )
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)
