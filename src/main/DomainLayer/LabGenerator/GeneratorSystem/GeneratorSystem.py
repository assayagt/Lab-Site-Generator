from src.main.DomainLayer.LabGenerator.User.UserFacade import UserFacade

class GeneratorSystem:
    _singleton_instance = None

    def __init__(self):
        self.user_facade = UserFacade()

    @staticmethod
    def get_instance():
        if GeneratorSystem._singleton_instance is None:
            GeneratorSystem._singleton_instance = GeneratorSystem()
        return GeneratorSystem._singleton_instance

    def login(self, userId, email):
        self.user_facade.error_if_user_notExist(userId)
        self.user_facade.login(userId, email)

    def logout(self, userId):
        self.user_facade.error_if_user_notExist(userId)
        self.user_facade.logout(userId)