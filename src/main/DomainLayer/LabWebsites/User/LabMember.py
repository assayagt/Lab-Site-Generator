from State import State
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from enum import Enum

class Degree(Enum):
    BACHELOR = "Bachelor's"
    MASTER = "Master's"
    PHD = "PhD"
    POSTDOC = "Postdoctoral"

class LabMember(State):
    def __init__(self, email, secondEmail=None, linkedin_link=None, media=None, fullName=None, user_id=None, degree=None, bio=None):
        self.email = email
        self.secondEmail = secondEmail
        self.linkedin_link = linkedin_link
        self.media = media
        self.fullName = fullName
        self.user_id = user_id
        self.degree = degree
        self.bio = bio

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

    def set_secondEmail(self, secondEmail):
        self.secondEmail = secondEmail

    def set_linkedin_link(self, linkedin_link):
        self.linkedin_link = linkedin_link

    def set_media(self, media):
        self.media = media

    def set_fullName(self, fullName):
        self.fullName = fullName

    def set_degree(self, degree):
        self.degree = degree

    def set_bio(self, bio):
        self.bio = bio

    def get_secondEmail(self):
        return self.secondEmail

    def get_linkedin_link(self):
        return self.linkedin_link

    def get_media(self):
        return self.media

    def get_fullName(self):
        return self.fullName

    def get_degree(self):
        return self.degree

    def get_bio(self):
        return self.bio


