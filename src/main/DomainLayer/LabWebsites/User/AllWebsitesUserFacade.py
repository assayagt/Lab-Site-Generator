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
        userFacade.error_if_labMember_notExist(nominated_manager_email)
        userFacade.create_new_site_manager(nominated_manager_email)

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.register_new_LabMember(email_to_register)

    def create_new_site_manager_from_generator(self, nominated_manager_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_labMember_notExist(nominated_manager_email)
        userFacade.create_new_site_manager(nominated_manager_email)

    def register_new_LabMember_from_generator(self, email_to_register, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.register_new_LabMember(email_to_register)

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



