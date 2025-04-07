import re

from src.main.DomainLayer.LabGenerator.User.Member import Member
from src.main.DomainLayer.LabGenerator.User.User import User
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.DAL.DAL_controller import DAL_controller
import uuid

class UserFacade:
    _singleton_instance = None

    def __init__(self):
        self.users = {}
        self.members_customSites = {} # sites that was created by the user <email, <Member, [domains]>> (both generated and not generated)
        self.dal_controller = DAL_controller()

    @staticmethod
    def get_instance():
        if UserFacade._singleton_instance is None:
            UserFacade._singleton_instance = UserFacade()
        return UserFacade._singleton_instance

    def create_new_site_manager(self, email, domain):
        #check if key in self.members_customSites
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
        # Update domains in self.members_customSites
        for email, data in self.members_customSites.items():
            if old_domain in data["domains"]:
                data["domains"][data["domains"].index(old_domain)] = new_domain
                self.dal_controller.members_repo.save_domain(email=email, domain=new_domain) #=================
                self.dal_controller.members_repo.delete_domain(email=email, domain=old_domain) #=================

    def error_if_user_is_not_site_manager(self, userId, domain):
        email = self.get_email_by_userId(userId)
        #check if domain is one of the sites that the user is a manager of
        if domain not in self.members_customSites[email]["domains"]:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def check_if_email_is_site_manager(self, email, domain):
        if email in self.members_customSites:
            if domain in self.members_customSites[email]["domains"]:
                return True
        return False

    def error_if_email_is_not_valid(self, email):
        """
        Validate the email format using a regular expression.
        Raise an error if the email is not valid.
        """
        email_regex = (
            r"^(?!.*\.\.)(?!.*\.$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
        if re.match(email_regex, email) is  None:
            raise Exception(ExceptionsEnum.INVALID_EMAIL_FORMAT.value)

    def login(self, userId, email):
        """Handle login logic after retrieving user info."""
        user = self.get_user_by_id(userId)
        member = self.get_member_by_email(email)
        if member is not None:
            member.set_user_id(userId)
        else:
            member = Member(user_id=userId, email=email)
            self.members_customSites[email] = {"member": member, "domains": []}
            self.dal_controller.members_repo.save_member(email) #=================

        user.login(member)

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
        self.users[user_id] = user
        return user_id

    def get_lab_websites(self, user_id):
        """Get all lab websites."""
        email = self.get_email_by_userId(user_id)
        return self.members_customSites[email]["domains"]

    def reset_system(self):
        """
        Resets the entire system by clearing all users, members, and site-related data.
        """
        self.users.clear()
        self.members_customSites.clear()

    def remove_site_manager(self, manager_toRemove_email, domain):
        #remove domain from the removed_manager_email
        if manager_toRemove_email in self.members_customSites:
            if domain in self.members_customSites[manager_toRemove_email]["domains"]:
                self.members_customSites[manager_toRemove_email]["domains"].remove(domain)
                self.dal_controller.members_repo.delete_domain_from_user(email=manager_toRemove_email, domain=domain)
            else:
                raise Exception(ExceptionsEnum.USER_IS_NOT_MANAGER_OF_THE_GIVEN_DOMAIN.value)
        else:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    
    def _load_all_members(self):
        member_emails = self.dal_controller.members_repo.find_all()
        for email in member_emails:
            member = Member(email=email)
            customs = self.dal_controller.siteCustom_repo.find_by_email(email)
            doms = [c.domain for c in customs] if customs else []
            self.members_customSites[email] = {"member": member, "domains": doms}
            

    
        