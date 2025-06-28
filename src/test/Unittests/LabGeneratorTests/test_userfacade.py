import unittest
from unittest.mock import patch, MagicMock, Mock
from src.main.DomainLayer.LabGenerator.User.UserFacade import UserFacade
from src.main.DomainLayer.LabGenerator.User.Member import Member
from src.main.DomainLayer.LabGenerator.User.User import User
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestUserFacade(unittest.TestCase):
    def setUp(self):
        UserFacade.reset_instance()
        self.facade = UserFacade()
        self.facade.dal_controller = Mock()
        self.facade.users = {}
        self.facade.members_customSites = {}

    def test_singleton(self):
        f1 = UserFacade.get_instance()
        f2 = UserFacade.get_instance()
        self.assertIs(f1, f2)

    def test_reset_instance(self):
        f1 = UserFacade.get_instance()
        UserFacade.reset_instance()
        f2 = UserFacade.get_instance()
        self.assertIsNot(f1, f2)

    def test_create_new_site_manager(self):
        self.facade.dal_controller.members_repo = Mock()
        self.facade.create_new_site_manager('a@test.com', 'd.com')
        self.assertIn('a@test.com', self.facade.members_customSites)
        self.assertIn('d.com', self.facade.members_customSites['a@test.com']['domains'])
        self.facade.dal_controller.members_repo.save_member.assert_called()
        self.facade.dal_controller.members_repo.save_domain.assert_called()

    def test_create_new_site_managers(self):
        self.facade.dal_controller.members_repo = Mock()
        self.facade.create_new_site_managers(['a@test.com', 'b@test.com'], 'd.com')
        self.assertIn('a@test.com', self.facade.members_customSites)
        self.assertIn('b@test.com', self.facade.members_customSites)

    def test_add_user(self):
        user_id = self.facade.add_user()
        self.assertIn(user_id, self.facade.users)
        self.assertIsInstance(self.facade.users[user_id], User)

    def test_login_and_logout(self):
        user = Mock()
        member = Mock()
        self.facade.users['u1'] = user
        self.facade.get_member_by_email = Mock(return_value=member)
        self.facade.dal_controller.members_repo = Mock()
        self.facade.login('u1', 'm@test.com')
        user.login.assert_called_once_with(member)
        self.facade.logout('u1')
        user.logout.assert_called_once()

    def test_error_if_user_notExist(self):
        with self.assertRaises(Exception) as ctx:
            self.facade.error_if_user_notExist('notfound')
        self.assertEqual(str(ctx.exception), ExceptionsEnum.USER_NOT_EXIST.value)

    def test_error_if_user_not_logged_in(self):
        user = Mock()
        user.is_member.return_value = False
        self.facade.users['u1'] = user
        with self.assertRaises(Exception) as ctx:
            self.facade.error_if_user_not_logged_in('u1')
        self.assertEqual(str(ctx.exception), ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def test_get_member_by_email(self):
        member = Member(email='a@test.com')
        self.facade.members_customSites['a@test.com'] = {'member': member, 'domains': []}
        self.assertEqual(self.facade.get_member_by_email('a@test.com'), member)
        self.assertIsNone(self.facade.get_member_by_email('notfound@test.com'))

    def test_get_user_by_id(self):
        user = User(user_id='u1')
        self.facade.users['u1'] = user
        self.assertEqual(self.facade.get_user_by_id('u1'), user)
        self.assertIsNone(self.facade.get_user_by_id('notfound'))

    def test_get_email_by_userId(self):
        user = Mock()
        user.get_email.return_value = 'a@test.com'
        self.facade.users['u1'] = user
        self.assertEqual(self.facade.get_email_by_userId('u1'), 'a@test.com')

    def test_remove_site_manager(self):
        self.facade.dal_controller.members_repo = Mock()
        self.facade.members_customSites['a@test.com'] = {'member': Member(email='a@test.com'), 'domains': ['d.com']}
        self.facade.remove_site_manager('a@test.com', 'd.com')
        self.assertNotIn('d.com', self.facade.members_customSites['a@test.com']['domains'])
        self.facade.dal_controller.members_repo.delete_domain_from_user.assert_called_once()

    def test_delete_website(self):
        self.facade.dal_controller.members_repo = Mock()
        self.facade.members_customSites['a@test.com'] = {'member': Member(email='a@test.com'), 'domains': ['d.com']}
        user = Mock()
        user.get_email.return_value = 'a@test.com'
        self.facade.users['u1'] = user
        self.facade.delete_website('u1', 'd.com')
        self.assertNotIn('d.com', self.facade.members_customSites['a@test.com']['domains'])
        self.facade.dal_controller.members_repo.delete_domain_from_user.assert_called_once()

    def test_reset_system(self):
        self.facade.users = {'u1': Mock()}
        self.facade.members_customSites = {'a@test.com': {'member': Mock(), 'domains': ['d.com']}}
        self.facade.reset_system()
        self.assertEqual(self.facade.users, {})
        self.assertEqual(self.facade.members_customSites, {})

if __name__ == '__main__':
    unittest.main() 