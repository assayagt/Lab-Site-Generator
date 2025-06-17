import unittest
from unittest.mock import Mock, patch

from src.main.DomainLayer.LabWebsites.Website.Website import Website
from src.main.DomainLayer.LabWebsites.Website.ContactInfo import ContactInfo
from src.main.DomainLayer.LabGenerator.User.User import User

class TestWebsite(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_user = User("test_user", "test@example.com", "password123")
        self.test_contact = ContactInfo(
            email="contact@example.com",
            phone="123-456-7890",
            address="123 Test St"
        )
        self.test_website = Website(
            name="Test Website",
            description="Test Description",
            contact_info=self.test_contact,
            owner_id=self.test_user.username
        )

    def test_website_creation(self):
        """Test website creation with valid data."""
        self.assertEqual(self.test_website.name, "Test Website")
        self.assertEqual(self.test_website.description, "Test Description")
        self.assertEqual(self.test_website.contact_info, self.test_contact)
        self.assertEqual(self.test_website.owner_id, self.test_user.username)
        self.assertFalse(self.test_website.is_approved)

    def test_invalid_name(self):
        """Test website creation with invalid name."""
        with self.assertRaises(ValueError):
            Website(
                name="",
                description="Test Description",
                contact_info=self.test_contact,
                owner_id=self.test_user.username
            )

    def test_invalid_description(self):
        """Test website creation with invalid description."""
        with self.assertRaises(ValueError):
            Website(
                name="Test Website",
                description="",
                contact_info=self.test_contact,
                owner_id=self.test_user.username
            )

    def test_update_website_info(self):
        """Test updating website information."""
        new_name = "Updated Website"
        new_description = "Updated Description"
        self.test_website.update_info(name=new_name, description=new_description)
        self.assertEqual(self.test_website.name, new_name)
        self.assertEqual(self.test_website.description, new_description)

    def test_update_contact_info(self):
        """Test updating contact information."""
        new_contact = ContactInfo(
            email="new@example.com",
            phone="987-654-3210",
            address="456 New St"
        )
        self.test_website.update_contact_info(new_contact)
        self.assertEqual(self.test_website.contact_info, new_contact)

    def test_approval_workflow(self):
        """Test website approval workflow."""
        # Test approval
        self.test_website.approve()
        self.assertTrue(self.test_website.is_approved)
        
        # Test rejection
        self.test_website.reject("Invalid content")
        self.assertFalse(self.test_website.is_approved)
        self.assertEqual(self.test_website.rejection_reason, "Invalid content")

    def test_validate_ownership(self):
        """Test website ownership validation."""
        self.assertTrue(self.test_website.validate_ownership(self.test_user))
        
        other_user = User("other_user", "other@example.com", "password123")
        self.assertFalse(self.test_website.validate_ownership(other_user))

if __name__ == '__main__':
    unittest.main() 