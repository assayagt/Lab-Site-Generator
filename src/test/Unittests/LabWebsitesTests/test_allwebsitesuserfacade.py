import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.main.DomainLayer.LabWebsites.User.AllWebsitesUserFacade import AllWebsitesUserFacade
from src.main.DomainLayer.LabWebsites.User.UserFacade import UserFacade
from src.main.DomainLayer.LabWebsites.User.LabMember import LabMember
from src.main.DomainLayer.LabWebsites.User.User import User
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestAllWebsitesUserFacade(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Reset singleton before tests
        AllWebsitesUserFacade.reset_instance()
        UserFacade.reset_all_instances()
    
    def setUp(self):
        # Reset singletons before each test
        AllWebsitesUserFacade.reset_instance()
        UserFacade.reset_all_instances()
        self.facade = AllWebsitesUserFacade()
        
        # Mock DAL controller
        self.mock_dal = Mock()
        self.facade.dal_controller = self.mock_dal
        
        # Mock website repository
        self.mock_website_repo = Mock()
        self.mock_dal.website_repo = self.mock_website_repo
    
    def tearDown(self):
        # Reset singletons after each test
        AllWebsitesUserFacade.reset_instance()
        UserFacade.reset_all_instances()
    
    def set_mock_user_facade(self, domain, user_id=None):
        user_facade = Mock()
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        if user_id:
            user_facade.users = {user_id: Mock()}
            user_facade.get_email_by_userId.return_value = "member@test.com"
        return user_facade
    
    def test_singleton_pattern(self):
        facade1 = AllWebsitesUserFacade()
        facade2 = AllWebsitesUserFacade()
        self.assertIs(facade1, facade2)
    
    def test_get_instance(self):
        facade1 = AllWebsitesUserFacade.get_instance()
        facade2 = AllWebsitesUserFacade.get_instance()
        self.assertIs(facade1, facade2)
    
    def test_reset_instance(self):
        facade1 = AllWebsitesUserFacade()
        AllWebsitesUserFacade.reset_instance()
        facade2 = AllWebsitesUserFacade()
        self.assertIsNot(facade1, facade2)
    
    def test_initialization(self):
        self.assertIsNotNone(self.facade.usersFacades)
        self.assertIsNotNone(self.facade.dal_controller)
        self.assertTrue(self.facade._initialized)
    
    def test_error_if_domain_not_exist(self):
        domain = "nonexistent.com"
        self.mock_website_repo.find_by_domain.return_value = None
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_domain_not_exist(domain)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)
        try:
            self.mock_website_repo.find_by_domain.assert_called_once_with(domain=domain)
        except AssertionError:
            self.mock_website_repo.find_by_domain.assert_called_once_with(domain)
    
    def test_error_if_domain_exists(self):
        domain = "existing.com"
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        # Should not raise exception
        self.facade.error_if_domain_not_exist(domain)
    
    def test_get_user_facade_by_domain_existing(self):
        domain = "test.com"
        user_facade = UserFacade(domain)
        self.facade.usersFacades[domain] = user_facade
        
        result = self.facade.getUserFacadeByDomain(domain)
        self.assertEqual(result, user_facade)
    
    def test_get_user_facade_by_domain_new(self):
        domain = "new.com"
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.getUserFacadeByDomain(domain)
        
        self.assertIn(domain, self.facade.usersFacades)
        self.assertIsInstance(result, UserFacade)
        self.assertEqual(result.domain, domain)
    
    def test_get_user_facade_by_domain_not_exist(self):
        domain = "nonexistent.com"
        self.mock_website_repo.find_by_domain.return_value = None
        
        with self.assertRaises(Exception) as context:
            self.facade.getUserFacadeByDomain(domain)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)
    
    def test_logout(self):
        domain = "test.com"
        user_id = "user123"
        user_facade = Mock()
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        self.facade.logout(domain, user_id)
        
        user_facade.logout.assert_called_once_with(user_id)
    
    def test_approve_registration_request(self):
        domain = "test.com"
        manager_user_id = "manager123"
        requested_email = "newuser@test.com"
        requested_full_name = "New User"
        requested_degree = Degree.MSC
        
        user_facade = Mock()
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        self.facade.approve_registration_request(domain, manager_user_id, requested_email, requested_full_name, requested_degree)
        
        user_facade.error_if_user_notExist.assert_called_once_with(manager_user_id)
        user_facade.error_if_user_not_logged_in.assert_called_once_with(manager_user_id)
        user_facade.error_if_user_is_not_manager_or_site_creator.assert_called_once_with(manager_user_id)
        user_facade.approve_registration_request.assert_called_once_with(requested_email, requested_full_name, requested_degree)
    
    def test_reject_registration_request(self):
        domain = "test.com"
        manager_user_id = "manager123"
        requested_email = "newuser@test.com"
        
        user_facade = Mock()
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        self.facade.reject_registration_request(domain, manager_user_id, requested_email)
        
        user_facade.error_if_user_notExist.assert_called_once_with(manager_user_id)
        user_facade.error_if_user_not_logged_in.assert_called_once_with(manager_user_id)
        user_facade.error_if_user_is_not_manager_or_site_creator.assert_called_once_with(manager_user_id)
        user_facade.reject_registration_request.assert_called_once_with(requested_email)

    def test_get_member_email_by_name(self):
        domain = "test.com"
        author = "John Author"
        user_facade = self.set_mock_user_facade(domain)
        user_facade.getMemberEmailByName = Mock()
        self.facade.getMemberEmailByName(author, domain)
        user_facade.getMemberEmailByName.assert_called_once_with(author)
    
    def test_get_all_alumnis(self):
        domain = "test.com"
        expected_alumnis = {"alumni1@test.com": Mock(), "alumni2@test.com": Mock()}
        
        user_facade = Mock()
        user_facade.getAlumnis.return_value = expected_alumnis
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_all_alumnis(domain)
        
        user_facade.getAlumnis.assert_called_once()
        self.assertEqual(result, expected_alumnis)
    
    def test_get_all_lab_members(self):
        domain = "test.com"
        expected_members = {"member1@test.com": Mock(), "member2@test.com": Mock()}
        
        user_facade = Mock()
        user_facade.getMembers.return_value = expected_members
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_all_lab_members(domain)
        
        user_facade.getMembers.assert_called_once()
        self.assertEqual(result, expected_members)
    
    def test_get_all_lab_managers(self):
        domain = "test.com"
        managers = {"manager1@test.com": Mock(), "manager2@test.com": Mock()}
        site_creator = {"creator@test.com": Mock()}
        expected_all_managers = {**managers, **site_creator}
        
        user_facade = Mock()
        user_facade.getManagers.return_value = managers
        user_facade.getSiteCreator.return_value = site_creator
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_all_lab_managers(domain)
        
        user_facade.getManagers.assert_called_once()
        user_facade.getSiteCreator.assert_called_once()
        self.assertEqual(result, expected_all_managers)

    def test_add_user_to_website(self):
        domain = "test.com"
        user_facade = Mock()
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        self.facade.add_user_to_website(domain)
        
        user_facade.add_user.assert_called_once()
    
    def test_get_active_members_names(self):
        domain = "test.com"
        expected_names = ["John Member", "Jane Manager"]
        
        user_facade = Mock()
        user_facade.get_active_members_names.return_value = expected_names
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_active_members_names(domain)
        
        user_facade.get_active_members_names.assert_called_once()
        self.assertEqual(result, expected_names)
    
    def test_get_active_members_scholar_links(self):
        domain = "test.com"
        expected_links = ["http://scholar1.com", "http://scholar2.com"]
        
        user_facade = Mock()
        user_facade.get_active_members_scholar_links.return_value = expected_links
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_active_members_scholarLinks(domain)
        
        user_facade.get_active_members_scholar_links.assert_called_once()
        self.assertEqual(result, expected_links)
    
    def test_get_all_members_names(self):
        domain = "test.com"
        expected_names = ["John Member", "Jane Alumni"]
        
        user_facade = Mock()
        user_facade.get_all_members_names.return_value = expected_names
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_all_members_names(domain)
        
        user_facade.get_all_members_names.assert_called_once()
        self.assertEqual(result, expected_names)
    
    def test_get_pending_registration_emails(self):
        domain = "test.com"
        expected_emails = ["pending1@test.com", "pending2@test.com"]
        
        user_facade = Mock()
        user_facade.get_pending_registration_emails.return_value = expected_emails
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_pending_registration_emails(domain)
        
        user_facade.get_pending_registration_emails.assert_called_once()
        self.assertEqual(result, expected_emails)
    
    def test_get_all_lab_members_details(self):
        domain = "test.com"
        expected_details = [{"email": "member1@test.com", "name": "John"}, {"email": "member2@test.com", "name": "Jane"}]
        
        user_facade = Mock()
        user_facade.get_all_lab_members_details.return_value = expected_details
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_all_lab_members_details(domain)
        
        user_facade.get_all_lab_members_details.assert_called_once()
        self.assertEqual(result, expected_details)
    
    def test_get_all_lab_managers_details(self):
        domain = "test.com"
        expected_details = [{"email": "manager1@test.com", "name": "John"}, {"email": "manager2@test.com", "name": "Jane"}]
        
        user_facade = Mock()
        user_facade.get_all_lab_managers_details.return_value = expected_details
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_all_lab_managers_details(domain)
        
        user_facade.get_all_lab_managers_details.assert_called_once()
        self.assertEqual(result, expected_details)
    
    def test_get_all_alumnis_details(self):
        domain = "test.com"
        expected_details = [{"email": "alumni1@test.com", "name": "John"}, {"email": "alumni2@test.com", "name": "Jane"}]
        
        user_facade = Mock()
        user_facade.get_all_alumnis_details.return_value = expected_details
        self.facade.usersFacades[domain] = user_facade
        self.mock_website_repo.find_by_domain.return_value = Mock()
        
        result = self.facade.get_all_alumnis_details(domain)
        
        user_facade.get_all_alumnis_details.assert_called_once()
        self.assertEqual(result, expected_details)

    def test_get_full_name_by_email(self):
        domain = "test.com"
        email = "user@test.com"
        user_facade = self.set_mock_user_facade(domain)
        user_facade.get_fullName_by_email = Mock()
        self.facade.get_fullName_by_email(email, domain)
        user_facade.get_fullName_by_email.assert_called_once_with(email)

    def test_get_scholar_link_by_email(self):
        domain = "test.com"
        email = "user@test.com"
        user_facade = self.set_mock_user_facade(domain)
        user_facade.get_scholar_link_by_email = Mock()
        self.facade.get_scholar_link_by_email(email, domain)
        user_facade.get_scholar_link_by_email.assert_called_once_with(email)

if __name__ == '__main__':
    unittest.main() 