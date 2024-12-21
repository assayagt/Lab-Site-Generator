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

    def create_new_site_manager(self, nominated_manager_email):
        if nominated_manager_email in self.members:
            member = self.getLabMemberByEmail(nominated_manager_email)
            del self.members[nominated_manager_email]
        else:
            member = LabMember(nominated_manager_email)
        self.managers[nominated_manager_email] = member

    def getLabMemberByEmail(self, email):
        return self.members[email]

    def error_if_labMember_notExist(self, email):
        if email not in self.members:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)

    def register_new_LabMember(self, email):
        member = self.get_member_by_email(email)
        if member is not None:
            raise Exception(ExceptionsEnum.EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_MEMBER.value)
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
            user.login(member)

    def logout(self, userId):
        user = self.get_user_by_id(userId)
        user.logout()

    def get_email_by_userId(self, userId):
        user = self.get_user_by_id(userId)
        return user.get_email()

    def error_if_user_not_logged_in(self, userId):
        user = self.get_user_by_id(userId)
        if not user.is_member():
            raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER)

    def error_if_user_is_not_manager(self, userId):
        email = self.get_email_by_userId(userId)
        if email not in self.managers:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER)

    def get_member_by_email(self, email):
        """Retrieve an active Member object by email."""
        if email in self.members:
            return self.members[email]
        elif email in self.managers:
            return self.managers[email]
        # todo: verify if alumnis can log in
        # elif email in self.alumnis:
        #    return self.alumnis[email]
        elif email in self.siteCreator:
            return self.siteCreator[email]
        return None

    def delete_member_by_email(self, email):
        """Delete an active member by an email
        Site creator cant be deleted!"""
        if email in self.members:
            del self.members[email]
        elif email in self.managers:
            del self.managers[email]

    def get_user_by_id(self, userId):
        if userId in self.users:
            user = self.users[userId]
        else:
            user = None
        return user

    def error_if_user_notExist(self, userId):
        if self.get_user_by_id(userId) is None:
            raise Exception(ExceptionsEnum.USER_NOT_EXIST.value)

    def error_if_member_is_not_labMember_or_manager(self, email):
        if email not in self.members and email not in self.managers:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER)

    def error_if_user_is_not_labMember_manager_creator(self, userId):
        email = self.get_email_by_userId(userId)
        if email not in self.members and email not in self.managers and email not in self.siteCreator:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER_OR_CREATOR)

    def define_member_as_alumni(self, email):
        if email in self.siteCreator:
            raise Exception(ExceptionsEnum.SITE_CREATOR_CANT_BE_ALUMNI)
        member = self.get_member_by_email(email)
        self.alumnis[email] = member
        self.delete_member_by_email(email)

    def get_manager_by_email(self, email):
        return self.managers[email]

    def remove_manager_permissions(self, email):
        if email not in self.managers:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER)
        manager = self.get_manager_by_email(email)
        self.members[email] = manager
        del self.managers[email]

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

    def set_site_creator(self, creator_email):
        member = LabMember(creator_email)
        self.siteCreator[creator_email] = member

    def set_secondEmail_by_member(self, email, secondEmail):
        member = self.get_member_by_email(email)
        member.set_secondEmail(secondEmail)

    def set_linkedin_link_by_member(self, email, linkedin_link):
        member = self.get_member_by_email(email)
        member.set_linkedin_link(linkedin_link)

    def set_media_by_member(self, email, media):
        member = self.get_member_by_email(email)
        member.set_media(media)

    def set_fullName_by_member(self,email, fullName):
        member = self.get_member_by_email(email)
        member.set_fullName_by_member(fullName)

