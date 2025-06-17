import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the main directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../main')))

from DomainLayer.LabGenerator.User.Member import Member

class TestMember(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.member = Member("member_user", "member@example.com", "password123")

    def test_member_initialization(self):
        """Test if member initializes with correct attributes."""
        self.assertEqual(self.member.username, "member_user")
        self.assertEqual(self.member.email, "member@example.com")
        self.assertEqual(self.member.password, "password123")
        self.assertTrue(self.member.is_member())

    def test_member_validation(self):
        """Test member validation methods."""
        # Test valid member
        self.assertTrue(self.member.is_valid())
        
        # Test invalid email
        invalid_member = Member("member_user", "invalid_email", "password123")
        self.assertFalse(invalid_member.is_valid())

    def test_member_permissions(self):
        """Test member permission methods."""
        self.assertTrue(self.member.can_create_site())
        self.assertTrue(self.member.can_edit_site())
        self.assertTrue(self.member.can_delete_site())

    def test_member_update(self):
        """Test updating member information."""
        new_email = "new_member@example.com"
        self.member.update_email(new_email)
        self.assertEqual(self.member.email, new_email)

    def test_member_equality(self):
        """Test member equality comparison."""
        same_member = Member("member_user", "member@example.com", "password123")
        different_member = Member("different_member", "different@example.com", "password123")
        
        self.assertEqual(self.member, same_member)
        self.assertNotEqual(self.member, different_member)

if __name__ == '__main__':
    unittest.main() 