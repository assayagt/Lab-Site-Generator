from State import State
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class LabMember(State):
    def __init__(self, email, secondEmail=None, linkedin_link=None, media=None, fullName=None, user_id=None):
        self.email = email
        self.secondEmail = secondEmail
        self.linkedin_link = linkedin_link
        self.media = media
        self.fullName = fullName
        self.user_id = user_id

    def logout(self):
        # Do nothing
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