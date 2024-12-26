from Member import Member
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class UserFacade:
    _singleton_instance = None

    def __init__(self):
        self.users = {}
        self.members_sites = {} # sites that was already generated
        self.members_customSites = {}

    @staticmethod
    def get_instance():
        if UserFacade._singleton_instance is None:
            UserFacade._singleton_instance = UserFacade()
        return UserFacade._singleton_instance

    def create_new_site_manager(self, email, domain):
        if domain not in self.members_sites[email]:
            self.members_sites[email].append(domain)

    def create_new_customSite_manager(self, userId, domain):
        email = self.get_email_by_userId(userId)
        if domain not in self.members_customSites[email]["domains"]:
            self.members_customSites[email]["domains"].append(domain)

    def change_site_domain(self, old_domain, new_domain):
        # Update domains in self.members_sites
        for email, domains in self.members_sites.items():
            if old_domain in domains:
                domains[domains.index(old_domain)] = new_domain

        # Update domains in self.members_customSites
        for email, data in self.members_customSites.items():
            if old_domain in data["domains"]:
                data["domains"][data["domains"].index(old_domain)] = new_domain

    def error_if_user_is_not_site_manager(self, userId, domain):
        email = self.get_email_by_userId(userId)
        #check if domain is one of the sites that the user is a manager of
        if domain not in self.members_sites[email]:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def login(self, userId, email):
        """Handle login logic after retrieving user info."""
        user = self.get_user_by_id(userId)
        member = self.get_member_by_email(email)
        if member is not None:
            member.setUserId(userId)
        else:
            member = Member(user_id=userId, email=email)
            self.members_sites[email] = []
            self.members_customSites[email] = {"member": member, "domains": []}
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
            raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER)

    def get_email_by_userId(self, userId):
        user = self.get_user_by_id(userId)
        return user.get_email()