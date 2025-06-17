import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the main directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../main')))

from DomainLayer.LabWebsites.WebCrawler.WebCrawler import WebCrawler

class TestWebCrawler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.web_crawler = WebCrawler()

    def test_web_crawler_initialization(self):
        """Test if web crawler initializes correctly."""
        self.assertIsNotNone(self.web_crawler)

    def test_abstract_methods(self):
        """Test that abstract methods raise NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.web_crawler.crawl()

        with self.assertRaises(NotImplementedError):
            self.web_crawler.parse()

    def test_web_crawler_equality(self):
        """Test web crawler equality comparison."""
        another_crawler = WebCrawler()
        self.assertEqual(self.web_crawler, another_crawler)

if __name__ == '__main__':
    unittest.main() 