class AllWebsitesUserFacade:
    _singleton_instance = None

    def __init__(self):
        self.usersFacades = {} # key: website domain, value: userFacade

    @staticmethod
    def get_instance():
        if AllWebsitesUserFacade._singleton_instance is None:
            AllWebsitesUserFacade._singleton_instance = AllWebsitesUserFacade()
        return AllWebsitesUserFacade._singleton_instance

    def getUserFacadeByDomain(self, domain):
        return self.usersFacades[domain]

    def logout(self, domain, userId):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.logout(userId)

    def create_new_site_manager(self, nominator_manager_userId, nominated_manager_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(nominator_manager_userId)
        userFacade.error_if_user_not_logged_in(nominator_manager_userId)
        userFacade.error_if_labMember_notExist(nominated_manager_email)
        userFacade.create_new_site_manager(nominated_manager_email)

    def register_new_LabMember(self, manager_userId, email_to_register, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.register_new_LabMember(email_to_register)

    def getMemberEmailByName(self, author, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.getMemberEmailByName(author)

