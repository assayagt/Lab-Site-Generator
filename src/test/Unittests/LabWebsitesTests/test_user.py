import unittest
from src.main.DomainLayer.LabWebsites.User.User import User
from src.main.DomainLayer.LabWebsites.User.LabMember import LabMember
from src.main.DomainLayer.LabWebsites.User.Guest import Guest
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(user_id='u1')

    def test_initial_state_is_guest(self):
        self.assertIsInstance(self.user.state, Guest)
        self.assertTrue(self.user.is_guest)
        self.assertFalse(self.user.is_member())

    def test_set_state_to_member(self):
        member = LabMember(
            email='member@example.com',
            fullName='John Doe',
            degree='Ph.D.'
        )
        self.user.set_state(member)
        self.assertIs(self.user.state, member)
        self.assertFalse(self.user.is_guest)
        self.assertTrue(self.user.is_member())

    def test_logout_sets_state_to_guest(self):
        member = LabMember(
            email='member@example.com',
            fullName='John Doe',
            degree='Ph.D.'
        )
        self.user.set_state(member)
        self.user.logout()
        self.assertIsInstance(self.user.state, Guest)
        self.assertTrue(self.user.is_guest)

    def test_login_sets_state_to_member(self):
        member = LabMember(
            email='member@example.com',
            fullName='John Doe',
            degree='Ph.D.'
        )
        self.user.login(member)
        self.assertIs(self.user.state, member)
        self.assertFalse(self.user.is_guest)
        self.assertTrue(self.user.is_member())

    def test_get_email_delegates_to_state(self):
        member = LabMember(
            email='member@example.com',
            fullName='John Doe',
            degree='Ph.D.'
        )
        self.user.set_state(member)
        self.assertEqual(self.user.get_email(), 'member@example.com')
        self.user.logout()
        self.assertIsNone(self.user.get_email())

if __name__ == '__main__':
    unittest.main() 