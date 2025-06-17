import unittest
from unittest.mock import Mock, patch

from src.main.DomainLayer.LabGenerator.User.User import User
from src.main.DomainLayer.LabGenerator.User.Member import Member
from src.main.DomainLayer.LabGenerator.User.Guest import Guest

class TestUser(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_user = User("test_user", "test@example.com", "password123")
        self.test_member = Member("member_user", "member@example.com", "password123")
        self.test_guest = Guest("guest_user", "guest@example.com")

    def test_user_creation(self):
        """Test user creation with valid data."""
        self.assertEqual(self.test_user.username, "test_user")
        self.assertEqual(self.test_user.email, "test@example.com")
        self.assertEqual(self.test_user.password, "password123")

    def test_member_creation(self):
        """Test member creation with valid data."""
        self.assertEqual(self.test_member.username, "member_user")
        self.assertEqual(self.test_member.email, "member@example.com")
        self.assertEqual(self.test_member.password, "password123")
        self.assertTrue(self.test_member.is_member)

    def test_guest_creation(self):
        """Test guest creation with valid data."""
        self.assertEqual(self.test_guest.username, "guest_user")
        self.assertEqual(self.test_guest.email, "guest@example.com")
        self.assertFalse(self.test_guest.is_member)

    def test_invalid_username(self):
        """Test user creation with invalid username."""
        with self.assertRaises(ValueError):
            User("", "test@example.com", "password123")

    def test_invalid_email(self):
        """Test user creation with invalid email."""
        with self.assertRaises(ValueError):
            User("test_user", "invalid_email", "password123")

    def test_invalid_password(self):
        """Test user creation with invalid password."""
        with self.assertRaises(ValueError):
            User("test_user", "test@example.com", "")

    def test_update_user_info(self):
        """Test updating user information."""
        self.test_user.update_info(email="updated@example.com")
        self.assertEqual(self.test_user.email, "updated@example.com")

    def test_validate_credentials(self):
        """Test credential validation."""
        self.assertTrue(self.test_user.validate_credentials("password123"))
        self.assertFalse(self.test_user.validate_credentials("wrong_password"))

if __name__ == '__main__':
    unittest.main() 