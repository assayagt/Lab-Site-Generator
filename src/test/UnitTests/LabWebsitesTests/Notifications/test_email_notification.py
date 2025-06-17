import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the main directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../main')))

from DomainLayer.LabWebsites.Notifications.EmailNotification import EmailNotification

class TestEmailNotification(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.notification = EmailNotification(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body"
        )

    def test_notification_initialization(self):
        """Test if notification initializes with correct attributes."""
        self.assertEqual(self.notification.recipient, "test@example.com")
        self.assertEqual(self.notification.subject, "Test Subject")
        self.assertEqual(self.notification.body, "Test Body")
        self.assertFalse(self.notification.is_sent)

    def test_notification_validation(self):
        """Test notification validation methods."""
        # Test valid notification
        self.assertTrue(self.notification.is_valid())
        
        # Test invalid notification (empty recipient)
        invalid_notification = EmailNotification("", "Subject", "Body")
        self.assertFalse(invalid_notification.is_valid())

    def test_notification_update(self):
        """Test updating notification information."""
        new_subject = "Updated Subject"
        new_body = "Updated Body"
        
        self.notification.update_subject(new_subject)
        self.notification.update_body(new_body)
        
        self.assertEqual(self.notification.subject, new_subject)
        self.assertEqual(self.notification.body, new_body)

    def test_notification_send(self):
        """Test notification sending functionality."""
        with patch('smtplib.SMTP') as mock_smtp:
            # Configure the mock
            mock_smtp_instance = mock_smtp.return_value
            mock_smtp_instance.send_message.return_value = {}
            
            # Send the notification
            self.notification.send()
            
            # Verify the notification was sent
            self.assertTrue(self.notification.is_sent)
            mock_smtp_instance.send_message.assert_called_once()

    def test_notification_equality(self):
        """Test notification equality comparison."""
        same_notification = EmailNotification(
            "test@example.com",
            "Test Subject",
            "Test Body"
        )
        different_notification = EmailNotification(
            "different@example.com",
            "Different Subject",
            "Different Body"
        )
        
        self.assertEqual(self.notification, same_notification)
        self.assertNotEqual(self.notification, different_notification)

    def test_notification_representation(self):
        """Test notification string representation."""
        expected_str = "Email to test@example.com: Test Subject"
        self.assertEqual(str(self.notification), expected_str)

if __name__ == '__main__':
    unittest.main() 