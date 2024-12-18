from src.main.DomainLayer.LabWebsites.User.LabMember import LabMember
from src.main.Util.ExceptionsEnum import ExceptionsEnum


class UserFacade:
    _singleton_instance = None

    def __init__(self):
        self.users = {}
        self.members = {}
        self.managers = {}
        self.siteCreator = {}
        self.alumnis = {}

    @staticmethod
    def get_instance():
        if UserFacade._singleton_instance is None:
            UserFacade._singleton_instance = UserFacade()
        return UserFacade._singleton_instance

    def create_new_site_manager(self, email):
        member = self.getMemberByEmail(email)
        self.managers[email] = member
        del self.members[email]

    def getMemberByEmail(self, email):
        return self.members[email]

    def error_if_labMember_notExist(self, email):
        member = self.members[email]
        if member is None:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)

    def registerNewLabMember(self, email):
        member = self.getMemberByEmail(email)
        if member is not None:
            raise Exception(ExceptionsEnum.EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_LAB_MEMBER.value)
        member = LabMember(email)
        self.members[email] = member

    def getMemberEmailByName(self, author):
        author_lower = author.lower()

        # Search in members
        for email, member in self.members.items():
            if member.fullName and member.fullName.lower() == author_lower:
                return member

        # Search in managers
        for email, manager in self.managers.items():
            if manager.fullName and manager.fullName.lower() == author_lower:
                return manager

        # Search in siteCreator
        for email, site_creator in self.siteCreator.items():
            if site_creator.fullName and site_creator.fullName.lower() == author_lower:
                return site_creator

        # If no match is found, return None
        return None

    def login(self, userId, email):
        """Handle login logic after retrieving user info."""
        user = self.get_user_by_id(userId)
        member = self.get_member_by_email(email)
        if member is not None:
            member.setUserId(userId)
        else:
            member = None
            #TODO: send notification to managers to approve or reject the registration
        user.login(member)

    def logout(self, userId):
        user = self.get_user_by_id(userId)
        user.logout()

    def get_member_by_email(self, email):
        """Retrieve a Member object by email."""
        if email in self.members:
            return self.members[email]
        elif email in self.managers:
            return self.managers[email]
        elif email in self.alumnis:
            return self.alumnis[email]
        elif email in self.siteCreator:
            return self.siteCreator[email]
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

    def getUsers(self):
        return self.users

    def getMembers(self):
        return self.members

    def getManagers(self):
        return self.managers

    def getSiteCreator(self):
        return self.siteCreator

    def getAlumnis(self):
        return self.alumnis

