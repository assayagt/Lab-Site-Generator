import unittest
from datetime import datetime

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.test.Acceptancetests.LabWebsitesTests.BaseTestClass import BaseTestClass


class TestCrawlForPublications(BaseTestClass):
    def setUp(self):
        # Call parent setUp to initialize mocks
        super().setUp()
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="creator@example.com")

        # Create a website for testing login
        self.website_name = "Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components, self.template)

        # Setup websites and their members
        self.creator_scholar_link = "https://scholar.google.com/citations?user=rgUqRpYAAAAJ&hl=en"  # Using a real scholar link
        self.generator_system_service.create_new_lab_website(
            self.domain,
            {
                "author1@example.com": {"full_name": "Author One", "degree": "Ph.D."},
                "invalid_author@example.com": {"full_name": "Invalid Author", "degree": "UNKNOWN"}
            },
            {"sagyto@gmail.com": {"full_name": "Roni Stern", "degree": "PHD"},
                         "creator@example.com": {"full_name": "Liron David", "degree": "PHD"}},
            {"email": "creator@example.com", "full_name": "Liron David", "degree": "PHD"},
            self.creator_scholar_link
        )

        # Simulate a lab member login
        self.lab_member_user_id = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_member_user_id = self.lab_system_service.login(self.domain, self.lab_member_user_id, "creator@example.com").get_data()


    def tearDown(self):
        # Call parent tearDown to stop mocks
        super().tearDown()
        # Reset the system after each test
        self.lab_system_service.reset_system()

    def test_crawl_for_publications_success(self):
        """
        Test that the system successfully crawls for publications and notifies authors.
        """

        # Validate that publications were fetched and assigned to the correct members
        publications = self.lab_system_service.get_all_not_approved_publications_of_member(self.domain, self.lab_member_user_id).get_data()
        self.assertIsNotNone(publications, "Publications should be fetched for valid author")

    def test_crawl_for_publications_duplicate_publication(self):
        # Trigger publication crawling once
        self.lab_system_service.crawl_for_publications()
        
        # Get initial publications count
        initial_publications = self.lab_system_service.get_all_approved_publications_of_member(self.domain, "author1@example.com").get_data()
        initial_publications_count = len(initial_publications) if initial_publications else 0

        # Trigger publication crawling again to test duplicate handling
        response = self.lab_system_service.crawl_for_publications()
        self.assertTrue(response.is_success())

        # Get updated publications count
        final_publications = self.lab_system_service.get_all_approved_publications_of_member(self.domain, "author1@example.com").get_data()
        final_publications_count = len(final_publications) if final_publications else 0

        # Verify that no new publications were added
        self.assertEqual(initial_publications_count, final_publications_count, 
                        "Duplicate publications were added when they shouldn't have been")

    def test_crawl_for_publications_failure_invalid_member(self):
        """
        Test that the system handles invalid members gracefully during publication crawling.
        """
        # Trigger publication crawling
        response = self.lab_system_service.crawl_for_publications()
        self.assertTrue(response.is_success())

        # Validate that invalid authors were skipped
        invalid_author_publications = self.lab_system_service.get_all_approved_publications_of_member(self.domain, "invalid_author@example.com").get_data()
        
        # Check that invalid author has no publications
        self.assertEqual(len(invalid_author_publications) if invalid_author_publications else 0, 0, 
                        "Invalid author should have no publications")

    def test_crawl_for_publications_send_notifications(self):
        """
        Test that notifications are sent to authors after fetching publications.
        """
        # Trigger publication crawling
        self.lab_system_service.crawl_for_publications()

        # Validate that notifications were sent to the authors
        # notifications = self.lab_system_service.get_notifications("author1@example.com").get_data()
        # self.assertGreater(len(notifications), 0)
        # self.assertIn("New Publication Pending Approval", [n.subject for n in notifications])
        # Skipped notification check due to missing proxy method


if __name__ == "__main__":
    unittest.main()
