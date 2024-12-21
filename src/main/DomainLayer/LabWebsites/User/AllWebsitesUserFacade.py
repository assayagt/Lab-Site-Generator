from UserFacade import UserFacade
class AllWebsitesUserFacade:
    _singleton_instance = None

    def __init__(self):
        self.usersFacades = {} # key: website domain, value: userFacade

    @staticmethod
    def get_instance():
        if AllWebsitesUserFacade._singleton_instance is None:
            AllWebsitesUserFacade._singleton_instance = AllWebsitesUserFacade()
        return AllWebsitesUserFacade._singleton_instance

    def add_new_webstie_userFacade(self, domain):
        self.usersFacades[domain] = UserFacade()

    def getUserFacadeByDomain(self, domain):
        return self.usersFacades[domain]

    def logout(self, domain, userId):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.logout(userId)

    def create_new_site_manager_from_labWebsite(self, nominator_manager_userId, nominated_manager_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(nominator_manager_userId)
        userFacade.error_if_user_not_logged_in(nominator_manager_userId)
        userFacade.error_if_user_is_not_manager(nominator_manager_userId)
        userFacade.error_if_labMember_notExist(nominated_manager_email)
        userFacade.create_new_site_manager(nominated_manager_email)

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager(manager_userId)
        userFacade.register_new_LabMember(email_to_register)

    def create_new_site_manager_from_generator(self, nominated_manager_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_labMember_notExist(nominated_manager_email)
        userFacade.create_new_site_manager(nominated_manager_email)

    def register_new_LabMember_from_generator(self, email_to_register, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.register_new_LabMember(email_to_register)

    def define_member_as_alumni(self, manager_userId, member_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager(manager_userId)
        userFacade.error_if_member_is_not_labMember_or_manager(member_email)
        userFacade.define_member_as_alumni(member_email)

    def remove_manager_permission(self, manager_userId, manager_toRemove_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager(manager_userId)
        userFacade.remove_manager_permissions(manager_toRemove_email)

    def getMemberEmailByName(self, author, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.getMemberEmailByName(author)

    def get_all_alumnis(self, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.getAlumnis()

    def get_all_lab_members(self, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.getMembers()

    def get_all_lab_managers(self, domain):
        """notice! this function returns all managers including site creator!"""
        userFacade = self.getUserFacadeByDomain(domain)
        managers = userFacade.getManagers()
        siteCreator = userFacade.getSiteCreator()
        return {**managers, **siteCreator}

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator(userid)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_secondEmail_by_member(email, secondEmail)

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator(userid)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_linkedin_link_by_member(email, linkedin_link)

    def set_media_by_member(self, userid, media, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator(userid)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_media_by_member(email, media)

    def set_fullName_by_member(self, userid, fullName, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator(userid)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_fullName_by_member(email, fullName)



