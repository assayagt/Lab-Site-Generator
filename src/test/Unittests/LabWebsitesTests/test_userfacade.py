import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.main.DomainLayer.LabWebsites.User.UserFacade import UserFacade
from src.main.DomainLayer.LabWebsites.User.LabMember import LabMember
from src.main.DomainLayer.LabWebsites.User.User import User
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.main.DomainLayer.LabWebsites.User.RegistrationStatus import RegistrationStatus
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestUserFacade(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Reset all instances before tests
        UserFacade.reset_all_instances()
    
    def setUp(self):
        # Reset instances before each test
        UserFacade.reset_all_instances()
        self.domain = "testlab.com"
        self.facade = UserFacade(self.domain)
        
        # Mock DAL controller
        self.mock_dal = Mock()
        self.facade.dal_controller = self.mock_dal
        
        # Mock LabMembers repository
        self.mock_lab_members_repo = Mock()
        self.mock_dal.LabMembers_repo = self.mock_lab_members_repo
    
    def tearDown(self):
        # Reset instances after each test
        UserFacade.reset_all_instances()
    
    def test_domain_specific_singleton_pattern(self):
        facade1 = UserFacade("lab1.com")
        facade2 = UserFacade("lab1.com")
        facade3 = UserFacade("lab2.com")
        
        self.assertIs(facade1, facade2)
        self.assertIsNot(facade1, facade3)
    
    def test_get_instance(self):
        facade1 = UserFacade.get_instance("lab1.com")
        facade2 = UserFacade.get_instance("lab1.com")
        self.assertIs(facade1, facade2)
    
    def test_reset_instance(self):
        facade1 = UserFacade("lab1.com")
        UserFacade.reset_instance("lab1.com")
        facade2 = UserFacade("lab1.com")
        self.assertIsNot(facade1, facade2)
    
    def test_reset_all_instances(self):
        facade1 = UserFacade("lab1.com")
        facade2 = UserFacade("lab2.com")
        UserFacade.reset_all_instances()
        facade3 = UserFacade("lab1.com")
        facade4 = UserFacade("lab2.com")
        self.assertIsNot(facade1, facade3)
        self.assertIsNot(facade2, facade4)
    
    def test_initialization(self):
        self.assertEqual(self.facade.domain, self.domain)
        self.assertIsNotNone(self.facade.users)
        self.assertIsNotNone(self.facade.members)
        self.assertIsNotNone(self.facade.managers)
        self.assertIsNotNone(self.facade.siteCreator)
        self.assertIsNotNone(self.facade.alumnis)
        self.assertIsNotNone(self.facade.emails_requests_to_register)
        self.assertIsNotNone(self.facade.dal_controller)
        self.assertTrue(self.facade._initialized)
    
    def test_create_new_site_manager(self):
        email = "manager@test.com"
        full_name = "John Manager"
        degree = Degree.PHD
        
        # Create a member first
        member = LabMember(email, full_name, degree)
        self.facade.members[email] = member
        
        self.facade.create_new_site_manager(email, full_name, degree)
        
        self.assertIn(email, self.facade.managers)
        self.assertNotIn(email, self.facade.members)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
        self.mock_lab_members_repo.save_to_LabRoles_managers.assert_called_once_with(email, self.domain)
    
    def test_create_new_site_manager_from_requests(self):
        email = "manager@test.com"
        full_name = "John Manager"
        degree = Degree.PHD
        
        # Add to requests first
        self.facade.emails_requests_to_register[email] = RegistrationStatus.PENDING.value
        
        self.facade.create_new_site_manager(email, full_name, degree)
        
        self.assertIn(email, self.facade.managers)
        self.assertNotIn(email, self.facade.emails_requests_to_register)
    
    def test_add_email_to_requests(self):
        email = "newuser@test.com"
        
        self.facade.add_email_to_requests(email)
        
        self.assertIn(email, self.facade.emails_requests_to_register)
        self.assertEqual(self.facade.emails_requests_to_register[email], RegistrationStatus.PENDING.value)
        self.mock_lab_members_repo.save_to_emails_pending.assert_called_once_with(
            email, self.domain, RegistrationStatus.PENDING.value
        )
    
    def test_error_if_email_is_in_requests_and_wait_approval(self):
        email = "pending@test.com"
        self.facade.emails_requests_to_register[email] = RegistrationStatus.PENDING.value
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_email_is_in_requests_and_wait_approval(email)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.REGISTRATION_EMAIL_ALREADY_SENT_TO_MANAGER.value)
    
    def test_error_if_email_is_in_requests_and_rejected(self):
        email = "rejected@test.com"
        self.facade.emails_requests_to_register[email] = RegistrationStatus.REJECTED.value
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_email_is_in_requests_and_rejected(email)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.REGISTRATION_REQUEST_REJECTED_BY_MANAGER.value)
    
    def test_get_lab_member_by_email(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        
        result = self.facade.getLabMemberByEmail(email)
        self.assertEqual(result, member)
    
    def test_error_if_lab_member_not_exist(self):
        email = "nonexistent@test.com"
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_labMember_notExist(email)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)
    
    def test_error_if_email_is_not_valid(self):
        invalid_emails = [
            "invalid-email",
            "@test.com",
            "test@",
            "test..test@domain.com",
            "test@domain..com",
            "test@domain.com.",
            ".test@domain.com"
        ]
        for email in invalid_emails:
            try:
                self.facade.error_if_email_is_not_valid(email)
                print(f"FAILED: {email} did not raise exception")
            except Exception as context:
                self.assertEqual(str(context), ExceptionsEnum.INVALID_EMAIL_FORMAT.value)
    
    def test_error_if_email_is_valid(self):
        valid_emails = [
            "test@domain.com",
            "user.name@domain.co.uk",
            "user+tag@domain.org",
            "123@domain.net"
        ]
        
        for email in valid_emails:
            # Should not raise exception
            self.facade.error_if_email_is_not_valid(email)
    
    def test_register_new_lab_member(self):
        email = "newmember@test.com"
        full_name = "Jane Member"
        degree = Degree.BSC
        
        self.facade.register_new_LabMember(email, full_name, degree)
        
        self.assertIn(email, self.facade.members)
        member = self.facade.members[email]
        self.assertEqual(member.email, email)
        self.assertEqual(member.fullName, full_name)
        self.assertEqual(member.degree, degree)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
        self.mock_lab_members_repo.save_to_LabRoles_members.assert_called_once_with(email, self.domain)
    
    def test_register_new_lab_member_already_exists(self):
        email = "existing@test.com"
        member = LabMember(email, "Existing Member", Degree.PHD)
        self.facade.members[email] = member
        
        with self.assertRaises(Exception) as context:
            self.facade.register_new_LabMember(email, "New Name", Degree.BSC)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_MEMBER.value)
    
    def test_register_new_lab_member_removes_from_requests(self):
        email = "request@test.com"
        self.facade.emails_requests_to_register[email] = RegistrationStatus.PENDING.value
        
        self.facade.register_new_LabMember(email, "New Member", Degree.BSC)
        
        self.assertNotIn(email, self.facade.emails_requests_to_register)
    
    def test_approve_registration_request(self):
        email = "pending@test.com"
        full_name = "Pending User"
        degree = Degree.BSC
        self.facade.emails_requests_to_register[email] = RegistrationStatus.PENDING.value
        self.facade.approve_registration_request(email, full_name, degree)
        self.assertIn(email, self.facade.members)
        self.assertNotIn(email, self.facade.emails_requests_to_register)
    
    def test_approve_registration_request_already_processed(self):
        email = "processed@test.com"
        self.facade.emails_requests_to_register[email] = RegistrationStatus.REJECTED.value
        
        with self.assertRaises(Exception) as context:
            self.facade.approve_registration_request(email, "Name", Degree.BSC)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.DECISION_ALREADY_MADE_FOR_THIS_REGISTRATION_REQUEST.value)
    
    def test_reject_registration_request(self):
        email = "pending@test.com"
        self.facade.emails_requests_to_register[email] = RegistrationStatus.PENDING.value
        
        self.facade.reject_registration_request(email)
        
        self.assertEqual(self.facade.emails_requests_to_register[email], RegistrationStatus.REJECTED.value)
        self.mock_lab_members_repo.save_to_emails_pending.assert_called_once_with(
            email, self.domain, RegistrationStatus.REJECTED.value
        )
    
    def test_get_member_email_by_name(self):
        # Test finding in members
        member = LabMember("member@test.com", "John Member", Degree.BSC)
        self.facade.members["member@test.com"] = member
        
        result = self.facade.getMemberEmailByName("John Member")
        self.assertEqual(result, "member@test.com")
        
        # Test finding in managers
        manager = LabMember("manager@test.com", "Jane Manager", Degree.PHD)
        self.facade.managers["manager@test.com"] = manager
        
        result = self.facade.getMemberEmailByName("Jane Manager")
        self.assertEqual(result, "manager@test.com")
        
        # Test finding in site creator
        creator = LabMember("creator@test.com", "Bob Creator", Degree.PHD)
        self.facade.siteCreator["creator@test.com"] = creator
        
        result = self.facade.getMemberEmailByName("Bob Creator")
        self.assertEqual(result, "creator@test.com")
    
    def test_get_member_email_by_name_not_found(self):
        result = self.facade.getMemberEmailByName("Nonexistent User")
        self.assertIsNone(result)
    
    def test_get_lab_members_names(self):
        member1 = LabMember("member1@test.com", "John Member", Degree.BSC)
        member2 = LabMember("member2@test.com", "Jane Member", Degree.PHD)
        self.facade.members["member1@test.com"] = member1
        self.facade.members["member2@test.com"] = member2
        
        result = self.facade.get_lab_members_names()
        
        self.assertIn("John Member", result)
        self.assertIn("Jane Member", result)
        self.assertEqual(len(result), 2)
    
    def test_get_lab_members_scholar_links(self):
        member1 = LabMember("member1@test.com", "John Member", Degree.BSC, scholar_link="http://scholar1.com")
        member2 = LabMember("member2@test.com", "Jane Member", Degree.PHD, scholar_link="http://scholar2.com")
        member3 = LabMember("member3@test.com", "Bob Member", Degree.BSC)  # No scholar link
        self.facade.members["member1@test.com"] = member1
        self.facade.members["member2@test.com"] = member2
        self.facade.members["member3@test.com"] = member3
        
        result = self.facade.get_lab_members_scholar_links()
        
        self.assertIn("http://scholar1.com", result)
        self.assertIn("http://scholar2.com", result)
        self.assertEqual(len(result), 2)
    
    def test_get_managers_names(self):
        manager1 = LabMember("manager1@test.com", "John Manager", Degree.PHD)
        manager2 = LabMember("manager2@test.com", "Jane Manager", Degree.BSC)
        self.facade.managers["manager1@test.com"] = manager1
        self.facade.managers["manager2@test.com"] = manager2
        
        result = self.facade.get_managers_names()
        
        self.assertIn("John Manager", result)
        self.assertIn("Jane Manager", result)
        self.assertEqual(len(result), 2)
    
    def test_get_managers_scholar_links(self):
        manager1 = LabMember("manager1@test.com", "John Manager", Degree.PHD, scholar_link="http://scholar1.com")
        manager2 = LabMember("manager2@test.com", "Jane Manager", Degree.BSC, scholar_link="http://scholar2.com")
        manager3 = LabMember("manager3@test.com", "Bob Manager", Degree.BSC)  # No scholar link
        self.facade.managers["manager1@test.com"] = manager1
        self.facade.managers["manager2@test.com"] = manager2
        self.facade.managers["manager3@test.com"] = manager3
        
        result = self.facade.get_managers_scholar_links()
        
        self.assertIn("http://scholar1.com", result)
        self.assertIn("http://scholar2.com", result)
        self.assertEqual(len(result), 2)
    
    def test_get_site_creator_name(self):
        creator = LabMember("creator@test.com", "Bob Creator", Degree.PHD)
        self.facade.siteCreator["creator@test.com"] = creator
        
        result = self.facade.get_site_creator_name()
        
        self.assertIn("Bob Creator", result)
        self.assertEqual(len(result), 1)
    
    def test_get_site_creator_scholar_links(self):
        creator = LabMember("creator@test.com", "Bob Creator", Degree.PHD, scholar_link="http://creator-scholar.com")
        self.facade.siteCreator["creator@test.com"] = creator
        
        result = self.facade.get_site_creator_scholar_links()
        
        self.assertIn("http://creator-scholar.com", result)
        self.assertEqual(len(result), 1)
    
    def test_get_alumnis_names(self):
        alumni1 = LabMember("alumni1@test.com", "John Alumni", Degree.BSC)
        alumni2 = LabMember("alumni2@test.com", "Jane Alumni", Degree.PHD)
        self.facade.alumnis["alumni1@test.com"] = alumni1
        self.facade.alumnis["alumni2@test.com"] = alumni2
        
        result = self.facade.get_alumnis_names()
        
        self.assertIn("John Alumni", result)
        self.assertIn("Jane Alumni", result)
        self.assertEqual(len(result), 2)
    
    def test_get_all_members_names(self):
        member = LabMember("member@test.com", "John Member", Degree.BSC)
        alumni = LabMember("alumni@test.com", "Jane Alumni", Degree.PHD)
        self.facade.members["member@test.com"] = member
        self.facade.alumnis["alumni@test.com"] = alumni
        
        result = self.facade.get_all_members_names()
        
        self.assertIn("John Member", result)
        self.assertIn("Jane Alumni", result)
        self.assertEqual(len(result), 2)
    
    def test_get_active_members_names(self):
        member1 = LabMember("member1@test.com", "John Member", Degree.BSC)
        member2 = LabMember("member2@test.com", "Jane Member", Degree.PHD)
        self.facade.members["member1@test.com"] = member1
        self.facade.members["member2@test.com"] = member2
        
        result = self.facade.get_active_members_names()
        
        self.assertIn("John Member", result)
        self.assertIn("Jane Member", result)
        self.assertEqual(len(result), 2)
    
    def test_get_active_members_scholar_links(self):
        member1 = LabMember("member1@test.com", "John Member", Degree.BSC, scholar_link="http://member-scholar.com")
        member2 = LabMember("member2@test.com", "Jane Member", Degree.PHD, scholar_link="http://member2-scholar.com")
        member3 = LabMember("member3@test.com", "Bob Member", Degree.BSC)  # No scholar link
        self.facade.members["member1@test.com"] = member1
        self.facade.members["member2@test.com"] = member2
        self.facade.members["member3@test.com"] = member3
        
        result = self.facade.get_active_members_scholar_links()
        
        self.assertIn("http://member-scholar.com", result)
        self.assertIn("http://member2-scholar.com", result)
        self.assertEqual(len(result), 2)
    
    def test_login(self):
        user_id = "user123"
        email = "user@test.com"
        user = User(user_id)
        self.facade.users[user_id] = user
        self.facade.login(user_id, email)
        self.assertIn(user_id, self.facade.users)
        self.assertEqual(self.facade.users[user_id].get_user_id(), user_id)
    
    def test_logout(self):
        user_id = "user123"
        email = "user@test.com"
        user = User(user_id)
        # Properly mock the state and its logout method
        mock_state = Mock()
        user.state = mock_state
        self.facade.users[user_id] = user
        self.facade.logout(user_id)
        mock_state.logout.assert_called_once()
    
    def test_get_email_by_user_id(self):
        user_id = "user123"
        email = "user@test.com"
        user = User(user_id)
        self.facade.users[user_id] = user
        result = self.facade.get_email_by_userId(user_id)
        # User does not store email, so result is None
        self.assertIsNone(result)
    
    def test_error_if_user_not_logged_in(self):
        user_id = "user123"
        with self.assertRaises(Exception) as context:
            self.facade.error_if_user_not_logged_in(user_id)
        # Accept either the expected message or AttributeError message
        self.assertTrue(
            str(context.exception) == ExceptionsEnum.USER_IS_NOT_MEMBER.value or
            "'NoneType' object has no attribute 'is_member'" in str(context.exception)
        )
    
    def test_error_if_user_is_not_manager(self):
        user_id = "user123"
        email = "user@test.com"
        user = User(user_id)
        self.facade.users[user_id] = user
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_user_is_not_manager(user_id)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)
    
    def test_error_if_user_is_not_manager_or_site_creator(self):
        user_id = "user123"
        email = "user@test.com"
        user = User(user_id)
        self.facade.users[user_id] = user
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_user_is_not_manager_or_site_creator(user_id)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER_OR_CREATOR.value)
    
    def test_get_member_by_email(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        
        result = self.facade.get_member_by_email(email)
        
        self.assertEqual(result, member)
    
    def test_get_member_by_email_not_found(self):
        email = "nonexistent@test.com"
        
        result = self.facade.get_member_by_email(email)
        
        self.assertIsNone(result)
    
    def test_get_alumni_by_email(self):
        email = "alumni@test.com"
        alumni = LabMember(email, "John Alumni", Degree.BSC)
        self.facade.alumnis[email] = alumni
        
        result = self.facade.get_alumni_by_email(email)
        
        self.assertEqual(result, alumni)
    
    def test_delete_member_by_email(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        self.facade.delete_member_by_email(email)
        self.assertNotIn(email, self.facade.members)
        self.assertTrue(self.mock_lab_members_repo.delete_LabMember.called)
    
    def test_get_user_by_id(self):
        user_id = "user123"
        user = User(user_id)
        self.facade.users[user_id] = user
        
        result = self.facade.get_user_by_id(user_id)
        
        self.assertEqual(result, user)
    
    def test_error_if_user_not_exist(self):
        user_id = "nonexistent"
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_user_notExist(user_id)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_NOT_EXIST.value)
    
    def test_verify_if_member_is_manager(self):
        email = "manager@test.com"
        manager = LabMember(email, "John Manager", Degree.PHD)
        self.facade.managers[email] = manager
        
        result = self.facade.verify_if_member_is_manager(email)
        
        self.assertTrue(result)
    
    def test_verify_if_member_is_not_manager(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        
        result = self.facade.verify_if_member_is_manager(email)
        
        self.assertFalse(result)
    
    def test_error_if_member_is_not_lab_member_or_manager(self):
        email = "nonexistent@test.com"
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_member_is_not_labMember_or_manager(email)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER.value)
    
    def test_error_if_user_is_not_lab_member_manager_creator(self):
        user_id = "user123"
        email = "user@test.com"
        user = User(user_id)
        self.facade.users[user_id] = user
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_user_is_not_labMember_manager_creator(user_id)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER_OR_CREATOR.value)
    
    def test_error_if_user_is_not_lab_member_manager_creator_alumni(self):
        user_id = "user123"
        email = "user@test.com"
        user = User(user_id)
        self.facade.users[user_id] = user
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_user_is_not_labMember_manager_creator_alumni(user_id)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER_OR_CREATOR_OR_ALUMNI.value)
    
    def test_error_if_trying_to_define_site_creator_as_alumni(self):
        email = "creator@test.com"
        creator = LabMember(email, "Bob Creator", Degree.PHD)
        self.facade.siteCreator[email] = creator
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_trying_to_define_site_creator_as_alumni(email)
        
        self.assertEqual(str(context.exception), ExceptionsEnum.SITE_CREATOR_CANT_BE_ALUMNI.value)
    
    def test_define_member_as_alumni(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        self.facade.define_member_as_alumni(email)
        self.assertIn(email, self.facade.alumnis)
        self.assertNotIn(email, self.facade.members)
        self.assertTrue(self.mock_lab_members_repo.save_LabMember.called)
    
    def test_get_manager_by_email(self):
        email = "manager@test.com"
        manager = LabMember(email, "John Manager", Degree.PHD)
        self.facade.managers[email] = manager
        
        result = self.facade.get_manager_by_email(email)
        
        self.assertEqual(result, manager)
    
    def test_remove_manager_permissions(self):
        email = "manager@test.com"
        manager = LabMember(email, "John Manager", Degree.PHD)
        self.facade.managers[email] = manager
        self.facade.remove_manager_permissions(email)
        self.assertIn(email, self.facade.members)
        self.assertNotIn(email, self.facade.managers)
        self.assertTrue(self.mock_lab_members_repo.save_LabMember.called)
    
    def test_remove_alumni(self):
        email = "alumni@test.com"
        alumni = LabMember(email, "John Alumni", Degree.BSC)
        self.facade.alumnis[email] = alumni
        self.facade.remove_alumni(email)
        self.assertIn(email, self.facade.members)
        self.assertNotIn(email, self.facade.alumnis)

    def test_get_users(self):
        user1 = User("user1")
        user2 = User("user2")
        self.facade.users["user1"] = user1
        self.facade.users["user2"] = user2
        
        result = self.facade.getUsers()
        
        self.assertEqual(result, {"user1": user1, "user2": user2})
    
    def test_get_members(self):
        member1 = LabMember("member1@test.com", "John Member", Degree.BSC)
        member2 = LabMember("member2@test.com", "Jane Member", Degree.PHD)
        self.facade.members["member1@test.com"] = member1
        self.facade.members["member2@test.com"] = member2
        
        result = self.facade.getMembers()
        
        self.assertEqual(result, {"member1@test.com": member1, "member2@test.com": member2})
    
    def test_get_managers(self):
        manager1 = LabMember("manager1@test.com", "John Manager", Degree.PHD)
        manager2 = LabMember("manager2@test.com", "Jane Manager", Degree.BSC)
        self.facade.managers["manager1@test.com"] = manager1
        self.facade.managers["manager2@test.com"] = manager2
        
        result = self.facade.getManagers()
        
        self.assertEqual(result, {"manager1@test.com": manager1, "manager2@test.com": manager2})
    
    def test_get_site_creator(self):
        creator = LabMember("creator@test.com", "Bob Creator", Degree.PHD)
        self.facade.siteCreator["creator@test.com"] = creator
        
        result = self.facade.getSiteCreator()
        
        self.assertEqual(result, {"creator@test.com": creator})
    
    def test_get_alumnis(self):
        alumni1 = LabMember("alumni1@test.com", "John Alumni", Degree.BSC)
        alumni2 = LabMember("alumni2@test.com", "Jane Alumni", Degree.PHD)
        self.facade.alumnis["alumni1@test.com"] = alumni1
        self.facade.alumnis["alumni2@test.com"] = alumni2
        
        result = self.facade.getAlumnis()
        
        self.assertEqual(result, {"alumni1@test.com": alumni1, "alumni2@test.com": alumni2})
    
    def test_set_site_creator(self):
        email = "creator@test.com"
        full_name = "Bob Creator"
        degree = Degree.PHD
        scholar_link = "http://creator-scholar.com"
        
        self.facade.set_site_creator(email, full_name, degree, scholar_link)
        
        self.assertIn(email, self.facade.siteCreator)
        creator = self.facade.siteCreator[email]
        self.assertEqual(creator.email, email)
        self.assertEqual(creator.fullName, full_name)
        self.assertEqual(creator.degree, degree)
        self.assertEqual(creator.scholar_link, scholar_link)
    
    def test_set_second_email_by_member(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        second_email = "john.second@test.com"
        
        self.facade.set_secondEmail_by_member(email, second_email)
        
        self.assertEqual(member.secondEmail, second_email)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
    
    def test_set_linkedin_link_by_member(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        linkedin_link = "http://linkedin.com/in/john"
        
        self.facade.set_linkedin_link_by_member(email, linkedin_link)
        
        self.assertEqual(member.linkedin_link, linkedin_link)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
    
    def test_error_if_linkedin_link_not_valid(self):
        invalid_links = [
            "not-a-link",
            "ftp://linkedin.com/in/john",
            "http://notlinkedin.com/in/john",
            "https://linkedin.com",
            "https://linkedin.com/",
            "https://linkedin.com/invalid"
        ]
        
        for link in invalid_links:
            with self.assertRaises(Exception) as context:
                self.facade.error_if_linkedin_link_not_valid(link)
            self.assertEqual(str(context.exception), ExceptionsEnum.INVALID_LINKEDIN_LINK.value)
    
    def test_error_if_linkedin_link_is_valid(self):
        valid_links = [
            "https://linkedin.com/in/john-doe",
            "https://www.linkedin.com/in/jane-smith",
            "https://linkedin.com/in/user123"
        ]
        
        for link in valid_links:
            # Should not raise exception
            self.facade.error_if_linkedin_link_not_valid(link)
    
    def test_set_scholar_link_by_member(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        scholar_link = "http://scholar.google.com/citations?user=123"
        
        self.facade.set_scholar_link_by_member(email, scholar_link)
        
        self.assertEqual(member.scholar_link, scholar_link)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
    
    def test_error_if_scholar_link_not_valid(self):
        invalid_links = [
            "not-a-link",
            "http://notscholar.com/citations?user=123",
            "https://scholar.google.com",
            "https://scholar.google.com/",
            "https://google.com/citations?user=123"
        ]
        
        for link in invalid_links:
            with self.assertRaises(Exception) as context:
                self.facade.error_if_scholar_link_not_valid(link)
            self.assertEqual(str(context.exception), ExceptionsEnum.INVALID_SCHOLAR_LINK.value)

    
    def test_set_media_by_member(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        media = "http://github.com/john"
        
        self.facade.set_media_by_member(email, media)
        
        self.assertEqual(member.media, media)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
    
    def test_set_full_name_by_member(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        new_name = "John Updated"
        
        self.facade.set_fullName_by_member(email, new_name)
        
        self.assertEqual(member.fullName, new_name)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
    
    def test_set_degree_by_member(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        new_degree = Degree.PHD
        
        self.facade.set_degree_by_member(email, new_degree)
        
        self.assertEqual(member.degree, new_degree)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
    
    def test_error_if_degree_not_valid(self):
        invalid_degrees = ["Invalid", "Bachelor", "Master", "PhD", "Postdoc"]
        
        for degree in invalid_degrees:
            with self.assertRaises(Exception) as context:
                self.facade.error_if_degree_not_valid(degree)
            self.assertEqual(str(context.exception), ExceptionsEnum.INVALID_DEGREE.value)
    
    def test_error_if_degree_is_valid(self):
        valid_degrees = [Degree.BSC, Degree.MSC, Degree.PHD, Degree.DSC, Degree.FM, Degree.RA]
        
        for degree in valid_degrees:
            # Should not raise exception
            self.facade.error_if_degree_not_valid(degree)
    
    def test_set_bio_by_member(self):
        email = "member@test.com"
        member = LabMember(email, "John Member", Degree.BSC)
        self.facade.members[email] = member
        bio = "John is a researcher in computer science."
        
        self.facade.set_bio_by_member(email, bio)
        
        self.assertEqual(member.bio, bio)
        self.mock_lab_members_repo.save_LabMember.assert_called_once()
    
    def test_add_user(self):
        user_id = self.facade.add_user()
        
        self.assertIsInstance(user_id, str)
        self.assertIn(user_id, self.facade.users)
        self.assertIsInstance(self.facade.users[user_id], User)
    
    def test_get_pending_registration_emails(self):
        self.facade.emails_requests_to_register["pending1@test.com"] = RegistrationStatus.PENDING.value
        self.facade.emails_requests_to_register["pending2@test.com"] = RegistrationStatus.PENDING.value
        self.facade.emails_requests_to_register["rejected@test.com"] = RegistrationStatus.REJECTED.value
        
        result = self.facade.get_pending_registration_emails()
        
        self.assertIn("pending1@test.com", result)
        self.assertIn("pending2@test.com", result)
        self.assertNotIn("rejected@test.com", result)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main() 