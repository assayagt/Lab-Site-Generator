import unittest
from src.main.DomainLayer.LabGenerator.User.Member import Member
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestMember(unittest.TestCase):
    def setUp(self):
        self.member = Member(user_id='u123', email='member@example.com')

    def test_login_raises_exception(self):
        with self.assertRaises(Exception) as context:
            self.member.login()
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_ALREADY_LOGGED_IN.value)

    def test_is_member(self):
        self.assertTrue(self.member.is_member())

    def test_set_user_id(self):
        self.member.set_user_id('u456')
        self.assertEqual(self.member.user_id, 'u456')

    def test_get_member_id(self):
        self.assertEqual(self.member.get_member_id(), 'u123')

if __name__ == '__main__':
    unittest.main() 