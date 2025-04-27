import re
import threading
import uuid

from src.main.DomainLayer.LabGenerator.User.Member import Member
from src.main.DomainLayer.LabGenerator.User.User import User
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.DAL.DAL_controller import DAL_controller

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

        self._lock = threading.Lock()  # <-- add general lock for all access

        self.users = {}
        self.members_customSites = {}  # sites created by user <email, <Member, [domains]>>
        self.dal_controller = DAL_controller()
        self._load_all_members()

        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        with cls._instance_lock:
            cls._instance = None

    def create_new_site_manager(self, email, domain):
        with self._lock:
            if email not in self.members_customSites:
                member = Member(email=email)
                self.members_customSites[email] = {"member": member, "domains": []}
                self.dal_controller.members_repo.save_member(email)
            if domain not in self.members_customSites[email]["domains"]:
                self.members_customSites[email]["domains"].append(domain)
                self.dal_controller.members_repo.save_domain(email=email, domain=domain)

    def create_new_site_managers(self, lab_managers_emails, domain):
        for email in lab_managers_emails:
            self.create_new_site_manager(email, domain)

    def change_site_domain(self, old_domain, new_domain):
        with self._lock:
            for email, data in self.members_customSites.items():
                if old_domain in data["domains"]:
                    data["domains"][data["domains"].index(old_domain)] = new_domain
                    self.dal_controller.members_repo.save_domain(email=email, domain=new_domain)
                    self.dal_controller.members_repo.delete_domain(domain=old_domain)

    def error_if_user_is_not_site_manager(self, userId, domain):
        email = self.get_email_by_userId(userId)
        with self._lock:
            if domain not in self.members_customSites.get(email, {}).get("domains", []):
                raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def check_if_email_is_site_manager(self, email, domain):
        with self._lock:
            return email in self.members_customSites and domain in self.members_customSites[email]["domains"]

    def error_if_email_is_not_valid(self, email):
        email_regex = r"^(?!.*\\.\\.)(?!.*\\.$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        if re.match(email_regex, email) is None:
            raise Exception(ExceptionsEnum.INVALID_EMAIL_FORMAT.value)

    def login(self, userId, email):
        with self._lock:
            user = self.get_user_by_id(userId)
            member = self.get_member_by_email(email)
            if member is not None:
                member.set_user_id(userId)
            else:
                member = Member(user_id=userId, email=email)
                self.members_customSites[email] = {"member": member, "domains": []}
                self.dal_controller.members_repo.save_member(email)
            user.login(member)

    def logout(self, userId):
        with self._lock:
            user = self.get_user_by_id(userId)
            user.logout()

    def get_member_by_email(self, email):
        with self._lock:
            return self.members_customSites.get(email, {}).get("member")

    def get_user_by_id(self, userId):
        with self._lock:
            return self.users.get(userId)

    def error_if_user_notExist(self, userId):
        if self.get_user_by_id(userId) is None:
            raise Exception(ExceptionsEnum.USER_NOT_EXIST.value)

    def error_if_user_not_logged_in(self, userId):
        user = self.get_user_by_id(userId)
        if not user.is_member():
            raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def get_email_by_userId(self, userId):
        user = self.get_user_by_id(userId)
        return user.get_email()

    def add_user(self):
        user_id = str(uuid.uuid4())
        user = User(user_id=user_id)
        with self._lock:
            self.users[user_id] = user
        return user_id

    def get_lab_websites(self, user_id):
        email = self.get_email_by_userId(user_id)
        with self._lock:
            return self.members_customSites.get(email, {}).get("domains", [])

    def reset_system(self):
        with self._lock:
            self.users.clear()
            self.members_customSites.clear()

    def remove_site_manager(self, manager_toRemove_email, domain):
        with self._lock:
            if manager_toRemove_email in self.members_customSites:
                if domain in self.members_customSites[manager_toRemove_email]["domains"]:
                    self.members_customSites[manager_toRemove_email]["domains"].remove(domain)
                    self.dal_controller.members_repo.delete_domain_from_user(email=manager_toRemove_email, domain=domain)
                else:
                    raise Exception(ExceptionsEnum.USER_IS_NOT_MANAGER_OF_THE_GIVEN_DOMAIN.value)
            else:
                raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def _load_all_members(self):
        with self._lock:
            member_emails = self.dal_controller.members_repo.find_all()
            for email in member_emails:
                member = Member(email=email)
                customs = self.dal_controller.siteCustom_repo.find_by_email(email)
                doms = [c.domain for c in customs] if customs else []
                self.members_customSites[email] = {"member": member, "domains": doms}
