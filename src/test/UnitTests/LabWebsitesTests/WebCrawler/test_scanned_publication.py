import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the main directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../main')))

from DomainLayer.LabWebsites.WebCrawler.ScannedPublication import ScannedPublication

class TestScannedPublication(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.publication = ScannedPublication(
            title="Test Publication",
            authors=["Author 1", "Author 2"],
            year=2023,
            url="https://example.com/paper"
        )

    def test_publication_initialization(self):
        """Test if publication initializes with correct attributes."""
        self.assertEqual(self.publication.title, "Test Publication")
        self.assertEqual(self.publication.authors, ["Author 1", "Author 2"])
        self.assertEqual(self.publication.year, 2023)
        self.assertEqual(self.publication.url, "https://example.com/paper")

    def test_publication_validation(self):
        """Test publication validation methods."""
        # Test valid publication
        self.assertTrue(self.publication.is_valid())
        
        # Test invalid publication (empty title)
        invalid_publication = ScannedPublication("", ["Author 1"], 2023, "https://example.com")
        self.assertFalse(invalid_publication.is_valid())

    def test_publication_update(self):
        """Test updating publication information."""
        new_title = "Updated Publication"
        new_authors = ["New Author"]
        
        self.publication.update_title(new_title)
        self.publication.update_authors(new_authors)
        
        self.assertEqual(self.publication.title, new_title)
        self.assertEqual(self.publication.authors, new_authors)

    def test_publication_equality(self):
        """Test publication equality comparison."""
        same_publication = ScannedPublication(
            "Test Publication",
            ["Author 1", "Author 2"],
            2023,
            "https://example.com/paper"
        )
        different_publication = ScannedPublication(
            "Different Publication",
            ["Author 1"],
            2023,
            "https://example.com/different"
        )
        
        self.assertEqual(self.publication, same_publication)
        self.assertNotEqual(self.publication, different_publication)

    def test_publication_representation(self):
        """Test publication string representation."""
        expected_str = "Test Publication (2023) by Author 1, Author 2"
        self.assertEqual(str(self.publication), expected_str)

if __name__ == '__main__':
    unittest.main() 