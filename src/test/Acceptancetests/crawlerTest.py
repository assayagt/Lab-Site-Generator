import unittest
import sys
import os

# Step 1: Get the root directory (go up 3 levels from this test file)
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.insert(0, project_root)

# Now your src.* imports will work
from src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler import GoogleScholarWebCrawler
from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO

class TestFetchCrawlerPublicationsReal(unittest.TestCase):
    def setUp(self):
        self.crawler = GoogleScholarWebCrawler()  # Replace with your actual class name
        # Example Google Scholar profile with public publications
        self.valid_profile = "https://scholar.google.com/citations?user=H_pd61wAAAAJ&hl=en"  # Sample profile (public)

    def test_fetch_returns_publications(self):
        publications = self.crawler.fetch_crawler_publications([self.valid_profile])
        self.crawler.fill_details(publications)
        self.assertIsInstance(publications, list)
        for pub in publications:
            print(pub.to_dict())
        self.assertGreater(len(publications), 0)  # At least one publication found

        for pub in publications:
            self.assertIsInstance(pub, PublicationDTO)
            self.assertIsNotNone(pub.title)
            self.assertIsNotNone(pub.publication_year)
            self.assertEqual(pub.approved, ApprovalStatus.INITIAL_PENDING)

if __name__ == '__main__':
    unittest.main(verbosity=2)
