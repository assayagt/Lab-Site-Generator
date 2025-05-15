import unittest

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum


class TestRemoveWebsite(unittest.TestCase):
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
        self.lab_members = {"member1@example.com": {"full_name": "Member One", "degree": "B.Sc."},
                            "member2@example.com": {"full_name": "Member Two", "degree": "M.Sc."}}
        self.lab_managers = {"manager1@example.com": {"full_name": "Manager One", "degree": "Ph.D."}}
        self.site_creator = {"email": "creator@example.com", "full_name": "Roni Stern", "degree": "Ph.D."}

        # Create the custom website first
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain,
                                                     self.components, self.template)
        lab_website_creation_response = self.generator_system_service.create_new_lab_website(self.domain,
                                                                                             self.lab_members,
                                                                                             self.lab_managers,
                                                                                             self.site_creator)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_removal(self):
        # Test successfully removing a manager
        response = self.generator_system_service.delete_website(self.user_id, self.domain)
        self.assertTrue(response.is_success())

    