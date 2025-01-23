import unittest

from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestCreateWebsiteAndLab(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a website to test site creation
        self.website_name = "My Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.lab_members = {"member1@example.com": {"full_name": "Member One", "degree": Degree.BSC}, "member2@example.com": {"full_name": "Member Two", "degree": Degree.MSC}}
        self.lab_managers = {"manager1@example.com": {"full_name": "Manager One", "degree": Degree.PHD}}
        self.site_creator = {"email": "creator@example.com", "full_name": "Site Creator", "degree": Degree.PHD}

        # Create the custom website first
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain,
                                                                self.components, self.template)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_creation(self):
        # Test successful creation of the lab website
        lab_website_creation_response = self.generator_system_service.create_new_lab_website(self.domain,
                                                                                             self.lab_members,
                                                                                             self.lab_managers,
                                                                                             self.site_creator)
        self.assertTrue(lab_website_creation_response.is_success())

    def test_website_not_exist(self):
        # Test trying to create a lab website when the website domain doesn't exist
        invalid_domain = "non_existent_domain.example.com"

        # Try creating the lab website with a non-existent domain
        lab_website_creation_response = self.generator_system_service.create_new_lab_website(invalid_domain,
                                                                                             self.lab_members,
                                                                                             self.lab_managers,
                                                                                             self.site_creator)
        self.assertFalse(lab_website_creation_response.is_success())
        self.assertEqual(lab_website_creation_response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)
