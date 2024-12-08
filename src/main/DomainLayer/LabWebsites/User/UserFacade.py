class UserFacade:
    _singleton_instance = None

    def __init__(self):
        if UserFacade._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        self.users = {}
        self.members = {}
        self.managers = {}
        self.siteCreators = {}
        self.alumnis = {}


    @staticmethod
    def get_instance():
        if UserFacade._singleton_instance is None:
            UserFacade._singleton_instance = UserFacade()
        return UserFacade._singleton_instance

    def create_new_site_manager(self, username, domain):
        pass