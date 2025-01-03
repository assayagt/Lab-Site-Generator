import unittest
from src.test.Acceptancetests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestCreateNewSiteManager(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="manager_1@example.com")
        self.user_id2 = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id2, email="nonManager@example.com")

        # Create a website to test site creation
        self.website_name = "My Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Publiccations"]
        self.template = Template.BASIC
        self.lab_member1_email = "member1@example.com"
        self.lab_member2_email = "member2@example.com"
        self.lab_members = {self.lab_member1_email: "Member One", self.lab_member2_email: "Member Two"}
        self.lab_managers = {"manager1@example.com": "Manager One"}
        self.site_creator = {"email": "creator@example.com", "full_name": "Site Creator"}

        self.generator_system_service.create_website(self.user_id, "Lab Website", self.domain, self.components, self.template)

        # Create the custom website first
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain,self.components, self.template)

        # Create a new lab website
        self.generator_system_service.create_new_lab_website(self.domain, self.lab_members, self.lab_managers, self.site_creator)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_create_new_site_manager_success(self):
        # Test successful creation of a new site manager
        response = self.generator_system_service.create_new_site_manager(self.user_id, self.lab_member1_email, self.domain)
        self.assertTrue(response.is_success())

    def test_user_not_logged_in(self):
        # Test trying to add a new site manager when the user is not logged in
        nominated_manager_email = "member_1@example.com"
        self.generator_system_service.logout(self.user_id)
        response = self.generator_system_service.create_new_site_manager(self.user_id, nominated_manager_email, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_nominated_member_is_not_lab_member(self):
        # Test creating a new site manager with a non-existent member
        nominated_manager_email = "non_existent_member@example.com"
        response = self.generator_system_service.create_new_site_manager(self.user_id, nominated_manager_email, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)

    def test_user_not_site_manager(self):
        # Test when the user trying to create a new site manager is not a site manager
        response = self.generator_system_service.create_new_site_manager(self.user_id2, self.lab_member1_email, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

