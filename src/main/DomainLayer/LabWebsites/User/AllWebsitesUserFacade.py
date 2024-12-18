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

    def create_new_site_manager(self, email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.create_new_site_manager(email)

    def registerNewLabMember(self, email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.registerNewLabMember(email)

    def getMemberEmailByName(self, author, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.getMemberEmailByName(author)


