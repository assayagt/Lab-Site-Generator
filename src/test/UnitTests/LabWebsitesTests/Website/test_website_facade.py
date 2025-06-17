import unittest
from unittest.mock import Mock, patch

from src.main.DomainLayer.LabWebsites.Website.WebsiteFacade import WebsiteFacade
from src.main.DomainLayer.LabWebsites.Website.Website import Website
from src.main.DomainLayer.LabWebsites.Website.ContactInfo import ContactInfo
from src.main.DomainLayer.LabGenerator.User.User import User

class TestWebsiteFacade(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.website_facade = WebsiteFacade()
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

    def test_create_website(self):
        """Test website creation."""
        with patch.object(self.website_facade, '_validate_website') as mock_validate:
            mock_validate.return_value = True
            result = self.website_facade.create_website(
                name="New Website",
                description="New Description",
                contact_info=self.test_contact,
                owner=self.test_user
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, Website)

    def test_get_website(self):
        """Test getting a website."""
        with patch.object(self.website_facade, '_get_website_by_id') as mock_get:
            mock_get.return_value = self.test_website
            result = self.website_facade.get_website("website_id")
            self.assertEqual(result, self.test_website)

    def test_update_website(self):
        """Test updating website information."""
        with patch.object(self.website_facade, '_validate_website') as mock_validate:
            mock_validate.return_value = True
            new_name = "Updated Website"
            new_description = "Updated Description"
            result = self.website_facade.update_website(
                self.test_website,
                name=new_name,
                description=new_description
            )
            self.assertEqual(result.name, new_name)
            self.assertEqual(result.description, new_description)

    def test_delete_website(self):
        """Test website deletion."""
        with patch.object(self.website_facade, '_validate_website') as mock_validate:
            mock_validate.return_value = True
            result = self.website_facade.delete_website(self.test_website)
            self.assertTrue(result)

    def test_get_user_websites(self):
        """Test getting all websites for a user."""
        with patch.object(self.website_facade, '_get_websites_by_owner') as mock_get:
            mock_get.return_value = [self.test_website]
            result = self.website_facade.get_user_websites(self.test_user)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], self.test_website)

    def test_update_contact_info(self):
        """Test updating website contact information."""
        with patch.object(self.website_facade, '_validate_website') as mock_validate:
            mock_validate.return_value = True
            new_contact = ContactInfo(
                email="new@example.com",
                phone="987-654-3210",
                address="456 New St"
            )
            result = self.website_facade.update_contact_info(
                self.test_website,
                new_contact
            )
            self.assertEqual(result.contact_info, new_contact)

    def test_approval_workflow(self):
        """Test website approval workflow."""
        with patch.object(self.website_facade, '_validate_website') as mock_validate:
            mock_validate.return_value = True
            # Test approval
            result = self.website_facade.approve_website(self.test_website)
            self.assertTrue(result.is_approved)
            
            # Test rejection
            result = self.website_facade.reject_website(self.test_website, "Invalid content")
            self.assertFalse(result.is_approved)
            self.assertEqual(result.rejection_reason, "Invalid content")

    def test_validate_ownership(self):
        """Test website ownership validation."""
        self.assertTrue(self.website_facade.validate_ownership(
            self.test_website,
            self.test_user
        ))
        
        other_user = User("other_user", "other@example.com", "password123")
        self.assertFalse(self.website_facade.validate_ownership(
            self.test_website,
            other_user
        ))

    def test_error_handling(self):
        """Test error handling in facade methods."""
        with patch.object(self.website_facade, '_validate_website') as mock_validate:
            mock_validate.return_value = False
            with self.assertRaises(ValueError):
                self.website_facade.create_website(
                    name="",
                    description="",
                    contact_info=self.test_contact,
                    owner=self.test_user
                )

if __name__ == '__main__':
    unittest.main() 