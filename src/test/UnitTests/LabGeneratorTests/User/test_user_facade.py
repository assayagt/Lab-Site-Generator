import unittest
from unittest.mock import Mock, patch

from src.main.DomainLayer.LabGenerator.User.UserFacade import UserFacade
from src.main.DomainLayer.LabGenerator.User.User import User
from src.main.DomainLayer.LabGenerator.User.Member import Member
from src.main.DomainLayer.LabGenerator.User.Guest import Guest

class TestUserFacade(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.user_facade = UserFacade()
        self.test_user = User("test_user", "test@example.com", "password123")
        self.test_member = Member("member_user", "member@example.com", "password123")

    def test_register_user(self):
        """Test user registration."""
        with patch.object(self.user_facade, '_validate_user') as mock_validate:
            mock_validate.return_value = True
            result = self.user_facade.register_user(
                username="new_user",
                email="new@example.com",
                password="password123"
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, User)

    def test_login(self):
        """Test user login."""
        with patch.object(self.user_facade, '_authenticate_user') as mock_auth:
            mock_auth.return_value = self.test_user
            result = self.user_facade.login("test_user", "password123")
            self.assertEqual(result, self.test_user)

    def test_logout(self):
        """Test user logout."""
        self.user_facade.current_user = self.test_user
        self.user_facade.logout()
        self.assertIsNone(self.user_facade.current_user)

    def test_promote_to_member(self):
        """Test promoting a user to member."""
        with patch.object(self.user_facade, '_validate_user') as mock_validate:
            mock_validate.return_value = True
            result = self.user_facade.promote_to_member(self.test_user)
            self.assertIsInstance(result, Member)

    def test_get_current_user(self):
        """Test getting current user."""
        self.user_facade.current_user = self.test_user
        result = self.user_facade.get_current_user()
        self.assertEqual(result, self.test_user)

    def test_is_authenticated(self):
        """Test authentication status check."""
        self.user_facade.current_user = self.test_user
        self.assertTrue(self.user_facade.is_authenticated())
        
        self.user_facade.current_user = None
        self.assertFalse(self.user_facade.is_authenticated())

    def test_is_member(self):
        """Test member status check."""
        self.user_facade.current_user = self.test_member
        self.assertTrue(self.user_facade.is_member())
        
        self.user_facade.current_user = self.test_user
        self.assertFalse(self.user_facade.is_member())

    def test_update_user_info(self):
        """Test updating user information."""
        with patch.object(self.user_facade, '_validate_user') as mock_validate:
            mock_validate.return_value = True
            new_email = "updated@example.com"
            result = self.user_facade.update_user_info(
                self.test_user,
                email=new_email
            )
            self.assertEqual(result.email, new_email)

    def test_delete_user(self):
        """Test user deletion."""
        with patch.object(self.user_facade, '_validate_user') as mock_validate:
            mock_validate.return_value = True
            result = self.user_facade.delete_user(self.test_user)
            self.assertTrue(result)

    def test_error_handling(self):
        """Test error handling in facade methods."""
        with patch.object(self.user_facade, '_validate_user') as mock_validate:
            mock_validate.return_value = False
            with self.assertRaises(ValueError):
                self.user_facade.register_user(
                    username="invalid",
                    email="invalid",
                    password="invalid"
                )

if __name__ == '__main__':
    unittest.main() 