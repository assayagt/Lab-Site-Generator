import unittest
from src.main.DomainLayer.LabGenerator.User.Guest import Guest
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestGuest(unittest.TestCase):
    def setUp(self):
        self.guest = Guest()

    def test_logout_raises_exception(self):
        with self.assertRaises(Exception) as context:
            self.guest.logout()
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_login_does_nothing(self):
        # Should not raise
        self.guest.login()

    def test_is_member(self):
        self.assertFalse(self.guest.is_member())

    def test_get_email(self):
        self.assertIsNone(self.guest.get_email())

if __name__ == '__main__':
    unittest.main() 