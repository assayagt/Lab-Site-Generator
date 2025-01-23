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

    def test_register_new_lab_member_success(self):
        # Test successful registration of a new lab member
        response = self.generator_system_service.register_new_LabMember_from_generator(self.manager_user_id, self.lab_member_email, self.lab_member_full_name, self.lab_member_degree, self.domain)
        self.assertTrue(response.is_success())

    def test_user_not_logged_in(self):
        # Test trying to register a new lab member when the user is not logged in
        self.generator_system_service.logout(self.manager_user_id)
        response = self.generator_system_service.register_new_LabMember_from_generator(self.manager_user_id, self.lab_member_email, self.lab_member_full_name, self.lab_member_degree, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_user_not_site_manager(self):
        # Test when the user trying to register a new lab member is not a site manager
        response = self.generator_system_service.register_new_LabMember_from_generator(self.user_id2, self.lab_member_email, self.lab_member_full_name, self.lab_member_degree, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def test_email_already_associated_with_a_member(self):
        # Test trying to register a lab member with an email already associated with an existing member
        existing_member_email = "member1@example.com"
        response = self.generator_system_service.register_new_LabMember_from_generator(self.manager_user_id, existing_member_email, "Existing Lab Member", self.lab_member_degree, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_MEMBER.value)

    def test_email_associated_with_creator_or_manager(self):
        # Test trying to register a new lab member with an email already associated with a creator or manager
        response = self.generator_system_service.register_new_LabMember_from_generator(self.manager_user_id, "manager1@example.com", "Manager One", self.lab_member_degree, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_MEMBER.value)

    def test_degree_is_not_valid(self):
        # Test trying to register a new lab member with an invalid degree
        response = self.generator_system_service.register_new_LabMember_from_generator(self.manager_user_id, self.lab_member_email, self.lab_member_full_name, "Invalid Degree", self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_DEGREE.value)

    def test_email_is_not_valid(self):
        # Test trying to register a new lab member with an invalid email
        response = self.generator_system_service.register_new_LabMember_from_generator(self.manager_user_id, "invalid_email", self.lab_member_full_name, self.lab_member_degree, self.domain)
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.INVALID_EMAIL_FORMAT.value)