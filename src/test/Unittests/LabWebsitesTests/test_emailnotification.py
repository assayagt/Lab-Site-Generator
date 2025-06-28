import unittest
from unittest.mock import patch, MagicMock
from src.main.DomainLayer.LabWebsites.Notifications.EmailNotification import EmailNotification

class TestEmailNotification(unittest.TestCase):
    def setUp(self):
        self.notification = EmailNotification(
            id='notif123',
            recipient='user@example.com',
            subject='Test Subject',
            body='Test Body',
            domain='lab.example.com',
            request_email='requester@example.com',
            publication_id='pub456'
        )

    def test_initialization(self):
        self.assertEqual(self.notification.id, 'notif123')
        self.assertEqual(self.notification.recipient, 'user@example.com')
        self.assertEqual(self.notification.subject, 'Test Subject')
        self.assertEqual(self.notification.body, 'Test Body')
        self.assertEqual(self.notification.domain, 'lab.example.com')
        self.assertEqual(self.notification.request_email, 'requester@example.com')
        self.assertEqual(self.notification.publication_id, 'pub456')
        self.assertFalse(self.notification.isRead)

    def test_get_is_read(self):
        self.assertFalse(self.notification.get_is_read())
        self.notification.mark_as_read()
        self.assertTrue(self.notification.get_is_read())

    def test_get_subject(self):
        self.assertEqual(self.notification.get_subject(), 'Test Subject')

    def test_get_body(self):
        self.assertEqual(self.notification.get_body(), 'Test Body')

    def test_get_request_email(self):
        self.assertEqual(self.notification.get_request_email(), 'requester@example.com')

    def test_mark_as_read(self):
        self.assertFalse(self.notification.isRead)
        self.notification.mark_as_read()
        self.assertTrue(self.notification.isRead)

    def test_to_dict(self):
        notification_dict = self.notification.to_dict()
        self.assertEqual(notification_dict['id'], 'notif123')
        self.assertEqual(notification_dict['subject'], 'Test Subject')
        self.assertEqual(notification_dict['body'], 'Test Body')

    def test_to_dto(self):
        dto = self.notification.to_dto()
        self.assertEqual(dto.domain, 'lab.example.com')
        self.assertEqual(dto.id, 'notif123')
        self.assertEqual(dto.recipient, 'user@example.com')
        self.assertEqual(dto.subject, 'Test Subject')
        self.assertEqual(dto.body, 'Test Body')
        self.assertEqual(dto.request_email, 'requester@example.com')
        self.assertEqual(dto.publication_id, 'pub456')
        self.assertFalse(dto.isRead)

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.notification.send_email()
        
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('notifications.lab.website@gmail.com', 'ijtb kvpg efep srbu')
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main() 