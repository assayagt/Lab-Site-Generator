import re
import threading

from src.main.DomainLayer.LabGenerator.User.Member import Member
from src.main.DomainLayer.LabGenerator.User.User import User
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.DAL.DAL_controller import DAL_controller
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = (
    "894370088866-4jkvg622sluvf0k7cfv737tnjlgg00nt.apps.googleusercontent.com"
)


class UserFacade:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(UserFacade, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.users = {}
        self.members_customSites = {}  # sites created by user <email, <Member, [domains]>>
        self.dal_controller = DAL_controller()
        # self._load_all_members()  # =================== LAZY LOAD THAT
        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance. Useful for unit tests."""
        with cls._instance_lock:
            cls._instance = None

    def create_new_site_manager(self, email, domain):
        self.dal_controller.members_repo.save_member(email)
        self.dal_controller.members_repo.save_domain(email=email, domain=domain)

    def get_or_create_user_by_token(self, google_token):
        """
        This method validates the token exists, and then extracts email from the token
        and then get or create member by email (we trust the token because it was validated by google)
        """
        email = self.get_email_from_token(google_token=google_token)
        if not self.dal_controller.members_repo.find_by_email(email=email):
            self.dal_controller.members_repo.save_member(email=email)
        return email
    
    def get_email_from_token(self, google_token):
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            google_token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=2,
        )
        return idinfo["email"]


    def get_domains_by_email(self, email):
        customs = self.dal_controller.siteCustom_repo.find_by_email(email)
        doms = [c.domain for c in customs] if customs else []
        return doms

    def create_new_site_managers(self, lab_managers_emails, domain):
        for email in lab_managers_emails:
            self.create_new_site_manager(email, domain)

    def change_site_domain(self, old_domain, new_domain):
        # Update domains in self.members_customSites
        manager_emails = self.dal_controller.members_repo.find_by_domain(old_domain)
        self.dal_controller.members_repo.delete_domain(domain=old_domain)
        for email in manager_emails:
            self.dal_controller.members_repo.save_domain(email=email, domain=new_domain)

    def error_if_user_is_not_site_manager(self, google_token, domain):
        email = self.get_or_create_user_by_token(google_token)
        # check if domain is one of the sites that the user is a manager of
        if domain not in self.get_domains_by_email(email):
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def check_if_email_is_site_manager(self, email, domain):
        member_domains = self.dal_controller.members_repo.find_by_email(email)
        return domain in member_domains

    def logout(self, userId):
        user = self.get_user_by_id(userId)
        user.logout()

    def get_member_by_email(self, email):
        """Retrieve a Member object by email."""
        if email in self.members_customSites:
            return self.members_customSites[email]["member"]
        return None

    def get_user_by_id(self, userId):
        if userId in self.users:
            user = self.users[userId]
        else:
            user = None
        return user

    def error_if_user_notExist(self, userId):
        pass

    def error_if_user_not_logged_in(self, userId):
        try:
            self.get_email_from_token(google_token=userId)
        except Exception as e:
            raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def get_email_by_userId(self, userId):
        user = self.get_user_by_id(userId)
        return user.get_email()

    def add_user(self):
        user_id = str(uuid.uuid4())
        user = User(user_id=user_id)
        self.users[user_id] = user
        return user_id

    def get_lab_websites(self, user_id):
        """Get all lab websites."""
        email = self.get_email_from_token(user_id)
        return self.get_domains_by_email(email)

    def reset_system(self):
        """
        Resets the entire system by clearing all users, members, and site-related data.
        """
        self.users.clear()
        self.members_customSites.clear()

    def remove_site_manager(self, manager_toRemove_email, domain):
        # remove domain from the removed_manager_email
        if manager_toRemove_email in self.members_customSites:
            if domain in self.members_customSites[manager_toRemove_email]["domains"]:
                self.members_customSites[manager_toRemove_email]["domains"].remove(
                    domain
                )
                self.dal_controller.members_repo.delete_domain_from_user(
                    email=manager_toRemove_email, domain=domain
                )
            else:
                raise Exception(
                    ExceptionsEnum.USER_IS_NOT_MANAGER_OF_THE_GIVEN_DOMAIN.value
                )
        else:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def delete_website(self, user_id, domain):
        email = self.get_email_by_userId(user_id)
        # remove domain from the email
        if email in self.members_customSites:
            if domain in self.members_customSites[email]["domains"]:
                self.members_customSites[email]["domains"].remove(domain)
                self.dal_controller.members_repo.delete_domain_from_user(
                    email=email, domain=domain
                )
            else:
                raise Exception(
                    ExceptionsEnum.USER_IS_NOT_MANAGER_OF_THE_GIVEN_DOMAIN.value
                )
        else:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def _load_all_members(self):
        member_emails = self.dal_controller.members_repo.find_all()
        for email in member_emails:
            member = Member(email=email)
            customs = self.dal_controller.siteCustom_repo.find_by_email(email)
            doms = [c.domain for c in customs] if customs else []
            self.members_customSites[email] = {"member": member, "domains": doms}
