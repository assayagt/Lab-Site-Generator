import unittest
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabWebsites.User.Degree import Degree

class TestRegisterNewLabMember(unittest.TestCase):
    def setUp(self):
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
        self.lab_member_degree = Degree.PHD
        self.lab_members = {"member1@example.com": {"full_name": "Member One", "degree": Degree.MSC}, "member2@example.com": {"full_name": "Member Two", "degree": Degree.BSC}}
        self.lab_managers = {"manager1@example.com": {"full_name": "Manager One", "degree": Degree.PHD}}
        self.site_creator = {"email": "creator@example.com", "full_name": "Site Creator", "degree": Degree.PHD}

        # Create a new lab website
        self.generator_system_service.create_website(self.manager_user_id, "Lab Website", self.domain, ["Homepage", "Contact Us", "Publications"], Template.template1)
        self.generator_system_service.create_new_lab_website(self.domain, self.lab_members, self.lab_managers, self.site_creator)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_successful_website_creation(self):
        # Test creating a website successfully
        response = self.generator_system_service.site_creator_resignation(self.manager_user_id, self.domain, self.lab_member_email)
        self.assertTrue(response.is_success())

    def test_unsuccessful_no_site_creator(self):
        response = self.generator_system_service.site_creator_resignation(self.user_id2, self.domain,
                                                                          self.lab_member_email)
        self.assertFalse(response.is_success())