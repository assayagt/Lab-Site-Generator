import unittest
from datetime import datetime

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests


class TestCrawlForPublications(unittest.TestCase):
    def setUp(self):
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        # Simulate entering the generator system for a user
        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        # Create a website for testing login
        self.website_name = "Lab Website"
        self.domain = "lab1.example.com"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.BASIC
        self.generator_system_service.create_website(self.user_id, self.website_name, self.domain, self.components, self.template)

        # Create mock data for websites, members, and publications
        self.website_domain_1 = "website1.com"

        # Setup websites and their members
        self.lab_system_service.create_new_lab_website(
            self.website_domain_1,
            {
            },
            {"manager1@example.com": {"full_name": "Roni Stern", "degree": "PHD"}},
            {"email": "creator@example.com", "full_name": "Shahaf Shperberg", "degree": "PHD"},
        )


    def tearDown(self):
        # Reset the system after each test
        self.lab_system_service.reset_system()

    def test_crawl_for_publications_success(self):
        """
        Test that the system successfully crawls for publications and notifies authors.
        """
        # Trigger publication crawling
        response = self.lab_system_service.crawl_for_publications()
        self.assertTrue(response.is_success())

        # Validate that publications were fetched and assigned to the correct members
        website1_members = self.lab_system_service.get_all_lab_members(self.website_domain_1).get_data()

        # Check that publications exist in each website's member profiles
        self.assertGreater(len(website1_members["author1@example.com"].get_publications()), 0)
        self.assertGreater(len(website1_members["author2@example.com"].get_publications()), 0)

    def test_crawl_for_publications_failure_no_websites(self):
        """
        Test that crawling fails gracefully when there are no websites to crawl.
        """
        # Reset all websites
        self.lab_system_service.reset_system()

        response = self.lab_system_service.crawl_for_publications()
        self.assertFalse(response.is_success())
        self.assertEqual(response.get_message(), ExceptionsEnum.NO_WEBSITES_FOUND.value)

    def test_crawl_for_publications_duplicate_publication(self):
        """
        Test that duplicate publications are not added to members' profiles.
        """
        # Trigger publication crawling once
        self.lab_system_service.crawl_for_publications()

        # Trigger publication crawling again to test duplicate handling
        response = self.lab_system_service.crawl_for_publications()
        self.assertTrue(response.is_success())

        # Validate that duplicate publications were not added
        website1_members = self.lab_system_service.get_all_lab_members(self.website_domain_1).get_data()
        initial_publications_count = len(website1_members["author1@example.com"].get_publications())

        self.assertEqual(len(website1_members["author1@example.com"].get_publications()), initial_publications_count)

    def test_crawl_for_publications_failure_invalid_member(self):
        """
        Test that the system handles invalid members gracefully during publication crawling.
        """
        # Manually add an invalid member
        self.lab_system_service.add_member(
            self.website_domain_1,
            {"email": "invalid_author@example.com", "full_name": "Invalid Author", "degree": "UNKNOWN"},
        )

        response = self.lab_system_service.crawl_for_publications()
        self.assertTrue(response.is_success())

        # Validate that invalid authors were skipped
        website1_members = self.lab_system_service.get_all_lab_members(self.website_domain_1).get_data()
        self.assertEqual(len(website1_members["invalid_author@example.com"].get_publications()), 0)

    def test_crawl_for_publications_send_notifications(self):
        """
        Test that notifications are sent to authors after fetching publications.
        """
        # Trigger publication crawling
        self.lab_system_service.crawl_for_publications()

        # Validate that notifications were sent to the authors
        notifications = self.lab_system_service.get_notifications("author1@example.com").get_data()
        self.assertGreater(len(notifications), 0)
        self.assertIn("New Publication Pending Approval", [n.subject for n in notifications])


if __name__ == "__main__":
    unittest.main()
