import unittest
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestGetSiteByDomain(unittest.TestCase):
    def setUp(self):
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a website to test domain-based retrieval
        self.website_name = "My Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1


        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain,
                                                     self.components, self.template)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_get_site_by_domain_success(self):
        # Test successful retrieval of a website by domain
        response = self.generator_system_service.get_site_by_domain(self.domain)
        self.assertTrue(response.is_success())

        data = response.get_data()
        self.assertEqual(data['domain'], self.domain)
        self.assertEqual(data['name'], self.website_name)
        self.assertEqual(data['components'], self.components)
        self.assertEqual(data['template'], self.template.value)
        self.assertEqual(data['logo'], None)
        self.assertEqual(data['home_picture'], None)

    def test_get_site_by_invalid_domain(self):
        # Test retrieval of a non-existent domain
        invalid_domain = "non_existent_domain.example.com"
        response = self.generator_system_service.get_site_by_domain(invalid_domain)
        self.assertFalse(response.is_success())
