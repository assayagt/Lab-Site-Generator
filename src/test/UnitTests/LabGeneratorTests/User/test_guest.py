import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the main directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../main')))

from DomainLayer.LabGenerator.User.Guest import Guest

class TestGuest(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.guest = Guest()

    def test_guest_initialization(self):
        """Test if guest initializes with correct attributes."""
        self.assertFalse(self.guest.is_member())
        self.assertFalse(self.guest.is_authenticated())

    def test_guest_permissions(self):
        """Test guest permission methods."""
        self.assertFalse(self.guest.can_create_site())
        self.assertFalse(self.guest.can_edit_site())
        self.assertFalse(self.guest.can_delete_site())
        self.assertTrue(self.guest.can_view_sites())

    def test_guest_equality(self):
        """Test guest equality comparison."""
        another_guest = Guest()
        self.assertEqual(self.guest, another_guest)

    def test_guest_representation(self):
        """Test guest string representation."""
        self.assertEqual(str(self.guest), "Guest")

if __name__ == '__main__':
    unittest.main() 