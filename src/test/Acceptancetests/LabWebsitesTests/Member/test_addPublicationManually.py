import unittest

from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.Util.Response import Response
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.test.Acceptancetests.LabWebsitesTests.BaseTestClass import BaseTestClass

class TestAddPublicationManually(BaseTestClass):
    def setUp(self):
        # Call parent setUp to initialize mocks
        super().setUp()
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
        self.labMember1_name = "Guni Sharon"
        self.lab_managers = {
            "manager1@example.com": {"full_name": "Roni Stern", "degree": "Ph.D."},
        }
        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components,
                                                     self.template)
        self.generator_system_service.create_new_lab_website(
            self.domain, {self.labMember1_email: {"full_name": self.labMember1_name, "degree": "Ph.D."}},
            self.lab_managers,
            {"email": self.site_creator_email, "full_name": "Site Creator", "degree": "Ph.D."},
            ""
        )

        # Simulate a lab member login
        self.member_userId = self.lab_system_service.enter_lab_website(self.domain)
        self.member_userId = self.lab_system_service.login(self.domain, self.member_userId, self.labMember1_email).get_data()

        self.manager_id = self.lab_system_service.enter_lab_website(self.domain)
        self.manager_id = self.lab_system_service.login(self.domain, self.manager_id, "manager1@example.com").get_data()

    def tearDown(self):
        super().tearDown()
        # Reset the system after each test
        self.generator_system_service.reset_system()
        self.lab_system_service.reset_system()

    def test_add_publication_manually_success(self):
        """
        Test that a lab member can successfully add a new publication to the website.
        """
        # Prepare the publication details
        publication = PublicationDTO(
            title="Conflict-based search for optimal multi-agent pathfinding",
            authors=["member1@example.com", "author2@example.com"],
            publication_year=2015,
            approved=ApprovalStatus.APPROVED,
            publication_link="https://scholar.google.com/citations?view_op=view_citation&hl=en&user=X6t18NkAAAAJ&citation_for_view=X6t18NkAAAAJ:_kc_bZDykSQC"
        )
        authors_emails = ["member1@example.com", "author2@example.com"]

        # Perform the operation
        response = self.lab_system_service.add_publication_manually(
            self.manager_id, self.domain, publication.publication_link,
            None, None, None  # Pass None for git_link, video_link, and presentation_link if not provided
        )
        self.assertTrue(response.is_success())
        self.assertEqual(response.get_message(), "Publication added successfully")

        # Validate that the publication is now listed for the authors
        publications_member1 = self.lab_system_service.get_all_approved_publications_of_member(
            self.domain, self.member_userId
        ).get_data()
        #check if the titles of the publications are the same
        self.assertIn(publication.title, [pub["title"] for pub in publications_member1])

    def test_add_publication_manually_with_links_success(self):
        """
        Test that a lab member can successfully add a new publication to the website.
        """
        # Prepare the publication details
        publication = PublicationDTO(
            title="Conflict-based search for optimal multi-agent pathfinding",
            authors=["member1@example.com", "author2@example.com"],
            publication_year=2015,
            approved=True,
            publication_link="https://scholar.google.com/citations?view_op=view_citation&hl=en&user=X6t18NkAAAAJ&citation_for_view=X6t18NkAAAAJ:_kc_bZDykSQC"
        )
        authors_emails = ["member1@example.com", "author2@example.com"]

        # Perform the operation
        response = self.lab_system_service.add_publication_manually(
            self.manager_id, self.domain, publication.publication_link,
            "gitlink", "videolink", "presentationlink"  # Pass None for git_link, video_link, and presentation_link if not provided
        )
        self.assertTrue(response.is_success())
        self.assertEqual(response.get_message(), "Publication added successfully")

        # Validate that the publication is now listed for the authors
        publications_member1 = self.lab_system_service.get_all_approved_publications_of_member(
            self.domain, self.member_userId
        ).get_data()
        # check if the titles of the publications are the same
        self.assertIn(publication.title, [pub["title"] for pub in publications_member1])
        self.assertIn("gitlink", [pub["git_link"] for pub in publications_member1])
        self.assertIn("videolink", [pub["video_link"] for pub in publications_member1])
        self.assertIn("presentationlink", [pub["presentation_link"] for pub in publications_member1])

    def test_add_publication_manually_failure_website_not_exist(self):
        """
        Test that adding a publication to a non-existent website raises an error.
        """
        invalid_domain = "nonexistent.example.com"

        # Prepare the publication details
        publication = PublicationDTO(
            title="Nanotechnology Advances",
            authors=["member1@example.com"],
            publication_year=2025,
            approved=True,
            publication_link="http://example.com/nanotech"
        )
        authors_emails = ["member1@example.com"]

        # Attempt to perform the operation
        response = self.lab_system_service.add_publication_manually(
            self.member_userId, invalid_domain, publication.publication_link,
            None, None, None  # Pass None for git_link, video_link, and presentation_link if not provided
        )

        # Validate the exception
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)
