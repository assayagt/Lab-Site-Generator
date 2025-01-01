from src.main.DomainLayer.LabGenerator.User.State import State
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class Member(State):
    def __init__(self, user_id=None, email=None):
        self.user_id = user_id
        self.email = email

    def logout(self):
        # Do nothing
        pass

    def exit_Generator_system(self):
        pass

    def login(self):
        raise Exception(ExceptionsEnum.USER_ALREADY_LOGGED_IN.value)

    def get_email(self):
        return self.email

    def is_member(self):
        return True

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_member_id(self):
          return self.user_id
    
    def get_username(self):
        pass
