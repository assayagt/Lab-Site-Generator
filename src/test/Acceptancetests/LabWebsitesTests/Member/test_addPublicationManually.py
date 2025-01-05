import unittest
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.Util.Response import Response
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests


class TestAddPublicationManually(unittest.TestCase):
    def setUp(self):
        # Initialize the system with real data and components
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a lab website
        self.domain = "lab1.example.com"
        self.site_creator_email = "creator@example.com"
        self.labMember1_email = "member1@example.com"
        self.labMember1_name = "Member One"
        self.lab_managers = {
            "manager1@example.com": "Manager One",
        }
        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.BASIC
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)
        self.generator_system_service.create_new_lab_website(
            self.domain, {self.labMember1_email: self.labMember1_name}, self.lab_managers,
            {"email": self.site_creator_email, "full_name": "Site Creator"}
        )

        # Simulate a lab member login
        self.member_userId = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.member_userId, self.labMember1_email)

    def tearDown(self):
        # Reset the system after each test
        self.generator_system_service.reset_system()

    def test_add_publication_manually_success(self):
        """
        Test that a lab member can successfully add a new publication to the website.
        """
        # Prepare the publication details
        publication = PublicationDTO(
            paper_id="P12345",
            title="Research on AI",
            authors=["member1@example.com", "author2@example.com"],
            publication_year=2025,
            approved=True,
            publication_link="http://example.com/research-ai"
        )
        authors_emails = ["member1@example.com", "author2@example.com"]

        # Perform the operation
        response = self.lab_system_service.add_publication_manually(
            self.member_userId, publication, self.domain, authors_emails
        )
        self.assertTrue(response.is_success())

        # Validate that the publication is now listed for the authors
        publications_member1 = self.lab_system_service.get_all_approved_publications_of_member(
            self.domain, self.labMember1_email
        ).get_data()
        self.assertIn(publication, publications_member1)

    def test_add_publication_manually_failure_user_not_logged_in(self):
        """
        Test that a user who is not logged in cannot add a publication.
        """
        # Simulate a logout for the lab member
        self.lab_system_service.logout(self.domain, self.member_userId)

        # Prepare the publication details
        publication = PublicationDTO(
            paper_id="P12347",
            title="Advanced Robotics",
            authors=["member1@example.com"],
            publication_year=2025,
            approved=True,
            publication_link="http://example.com/advanced-robotics"
        )
        authors_emails = ["member1@example.com"]

        # Attempt to perform the operation
        response = self.lab_system_service.add_publication_manually(
            self.member_userId, publication, self.domain, authors_emails
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_add_publication_manually_failure_website_not_exist(self):
        """
        Test that adding a publication to a non-existent website raises an error.
        """
        invalid_domain = "nonexistent.example.com"

        # Prepare the publication details
        publication = PublicationDTO(
            paper_id="P12348",
            title="Nanotechnology Advances",
            authors=["member1@example.com"],
            publication_year=2025,
            approved=True,
            publication_link="http://example.com/nanotech"
        )
        authors_emails = ["member1@example.com"]

        # Attempt to perform the operation
        response = self.lab_system_service.add_publication_manually(
            self.member_userId, publication.to_dict(), invalid_domain, authors_emails
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)
