import unittest
from unittest.mock import patch, mock_open
from src.main.DomainLayer.LabWebsites.User.LabMember import LabMember, Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestLabMember(unittest.TestCase):
    def setUp(self):
        self.lab_member = LabMember(
            email='member@example.com',
            fullName='John Doe',
            degree=Degree.PHD,
            secondEmail='john.doe@example.com',
            linkedin_link='http://linkedin.com/johndoe',
            media='http://twitter.com/johndoe',
            user_id='u123',
            bio='Research scientist',
            scholar_link='http://scholar.google.com/johndoe',
            profile_picture='profile.jpg',
            email_notifications=True
        )

    def test_login_raises_exception(self):
        with self.assertRaises(Exception) as context:
            self.lab_member.login()
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_ALREADY_LOGGED_IN.value)

    def test_is_member(self):
        self.assertTrue(self.lab_member.is_member())

    def test_set_user_id(self):
        self.lab_member.set_user_id('u456')
        self.assertEqual(self.lab_member.user_id, 'u456')

    def test_get_details(self):
        details = self.lab_member.get_details()
        self.assertEqual(details['email'], 'member@example.com')
        self.assertEqual(details['fullName'], 'John Doe')
        self.assertEqual(details['degree'], Degree.PHD)
        self.assertEqual(details['secondEmail'], 'john.doe@example.com')
        self.assertEqual(details['linkedin_link'], 'http://linkedin.com/johndoe')
        self.assertEqual(details['media'], 'http://twitter.com/johndoe')
        self.assertEqual(details['bio'], 'Research scientist')
        self.assertEqual(details['scholar_link'], 'http://scholar.google.com/johndoe')
        self.assertEqual(details['email_notifications'], True)

    def test_get_dto(self):
        dto = self.lab_member.get_dto('lab.example.com')
        self.assertEqual(dto.domain, 'lab.example.com')
        self.assertEqual(dto.email, 'member@example.com')
        self.assertEqual(dto.full_name, 'John Doe')
        self.assertEqual(dto.degree, Degree.PHD)
        self.assertEqual(dto.second_email, 'john.doe@example.com')
        self.assertEqual(dto.linkedin_link, 'http://linkedin.com/johndoe')
        self.assertEqual(dto.media, 'http://twitter.com/johndoe')
        self.assertEqual(dto.bio, 'Research scientist')
        self.assertEqual(dto.scholar_link, 'http://scholar.google.com/johndoe')
        self.assertEqual(dto.profile_picture, 'profile.jpg')
        self.assertEqual(dto.email_notifications, True)

    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_image_data')
    @patch('os.path.exists', return_value=True)
    def test_get_encoded_profile_picture_png(self, mock_exists, mock_file):
        self.lab_member.profile_picture = 'profile.png'
        encoded = self.lab_member.get_encoded_profile_picture()
        self.assertIsNotNone(encoded)
        self.assertTrue(encoded.startswith('data:image/png;base64,'))

    @patch('os.path.exists', return_value=False)
    def test_get_encoded_profile_picture_not_exists(self, mock_exists):
        encoded = self.lab_member.get_encoded_profile_picture()
        self.assertIsNone(encoded)

    def test_set_email_notifications(self):
        self.lab_member.set_email_notifications(False)
        self.assertFalse(self.lab_member.get_email_notifications())

    def test_default_email_notifications(self):
        member_without_notifications = LabMember(
            email='member2@example.com',
            fullName='Jane Doe',
            degree=Degree.MASTER
        )
        self.assertTrue(member_without_notifications.get_email_notifications())

if __name__ == '__main__':
    unittest.main() 