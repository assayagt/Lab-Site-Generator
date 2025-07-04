import unittest
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.test.Acceptancetests.LabWebsitesTests.BaseTestClass import BaseTestClass
from src.main.DomainLayer.LabWebsites.User.Degree import Degree

class TestAddAlumniFromGenerator(BaseTestClass):
    def setUp(self):
        # Call parent setUp to initialize mocks
        super().setUp()
        # Initialize ProxyToTest with "Real"
        self.generator_system_service = ProxyToTest("Real")

        # Simulate entering the generator system for a user
        self.manager_user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.manager_user_id, email="manager_1@example.com")
        self.user_id2 = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id2, email="nonManager@example.com")

        # Set up lab members and website details
        self.domain = "lab1.example.com"
        self.lab_member_email = "new_member@example.com"
        self.lab_member_full_name = "New Lab Member"
        self.lab_member_degree = "Ph.D."
        self.lab_members = {"member1@example.com": {"full_name": "Member One", "degree": "M.Sc."}, "member2@example.com": {"full_name": "Member Two", "degree": "B.Sc."}}
        self.lab_managers = {"manager1@example.com": {"full_name": "Manager One", "degree": "Ph.D."}}
        self.site_creator = {"email": "creator@example.com", "full_name": "Liron David", "degree": "Ph.D."}
        self.creator_scholar_link = "https://scholar.google.com/citations?user=rgUqRpYAAAAJ&hl=en"

        # Create a new lab website
        self.generator_system_service.create_website(self.manager_user_id, "Lab Website", self.domain, ["Homepage", "Contact Us", "Publications"], Template.template1)
        self.generator_system_service.create_new_lab_website(self.domain, self.lab_members, self.lab_managers, self.site_creator, self.creator_scholar_link)

    def tearDown(self):
        # Call parent tearDown to stop mocks
        super().tearDown()
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_register_new_lab_member_success(self):
        # Test successful registration of a new lab member
        response = self.generator_system_service.add_alumni_from_generator(self.manager_user_id, "member1@example.com", self.domain)
        self.assertTrue(response.is_success())