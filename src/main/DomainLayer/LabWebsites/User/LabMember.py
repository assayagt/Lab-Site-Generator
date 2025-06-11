import base64
import os

from src.main.DomainLayer.LabWebsites.User.State import State
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from enum import Enum
from src.DAL.DTOs.LabMember_dto import lab_member_dto
class Degree(Enum):
    BACHELOR = "Bachelor's"
    MASTER = "Master's"
    PHD = "PhD"
    POSTDOC = "Postdoctoral"

class LabMember(State):
    def __init__(self, email, fullName, degree, secondEmail=None, linkedin_link=None, media=None, user_id=None, bio=None, scholar_link=None, profile_picture=None, email_notifications=None):
        self.email = email
        self.secondEmail = secondEmail
        self.linkedin_link = linkedin_link
        self.scholar_link = scholar_link
        self.media = media
        self.fullName = fullName
        self.user_id = user_id
        self.degree = degree
        self.bio = bio
        self.profile_picture = profile_picture
        #True if none else email_notifications
        self.email_notifications = email_notifications if email_notifications is not None else True

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

    def set_scholar_Link(self, scholarLink):
        self.scholar_link = scholarLink

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
    
    def get_scholarLink(self):
        return self.scholar_link

    def get_media(self):
        return self.media

    def get_fullName(self):
        return self.fullName

    def get_degree(self):
        return self.degree

    def get_bio(self):
        return self.bio

    def get_profile_picture(self):
        return self.profile_picture if self.profile_picture else None

    def set_profile_picture(self, file_path):
        self.profile_picture = file_path

    def set_email_notifications(self, email_notifications):
        self.email_notifications = email_notifications

    def get_email_notifications(self):
        return self.email_notifications

    #TODO: fix this method so support scholar link as well. I DID ITTTT
    def get_details(self):
        return {"email": self.email,
                "secondEmail": self.secondEmail,
                "linkedin_link": self.linkedin_link,
                "media": self.media,
                "fullName": self.fullName,
                "degree": self.degree,
                "bio": self.bio,
                "scholar_link": self.scholar_link,
                "profile_picture": self.get_encoded_profile_picture(),
                "email_notifications": self.email_notifications}

    def get_dto(self, domain) -> lab_member_dto:
        return lab_member_dto(
            domain=domain,
            email=self.email,
            second_email=self.secondEmail,
            linkedin_link=self.linkedin_link,
            scholar_link=  self.scholar_link,
            media=self.media,
            full_name=self.fullName,
            degree=self.degree,
            bio=self.bio,
            profile_picture=self.profile_picture,
            email_notifications=self.email_notifications
        )

    def get_encoded_profile_picture(self):
        if self.profile_picture and os.path.exists(self.profile_picture):
            # Check the file extension
            extension = os.path.splitext(self.profile_picture)[1].lower()
            if extension in ['.svg', '.png', '.jpg', '.jpeg']:
                with open(self.profile_picture, "rb") as profile_picture_file:
                    if extension == '.svg':
                        mime_type = 'image/svg+xml'
                    elif extension == '.png':
                        mime_type = 'image/png'
                    elif extension == '.jpg' or extension == '.jpeg':
                        mime_type = 'image/jpeg'
                    else:
                        mime_type = 'application/octet-stream'  # Default for unsupported types

                    logo_base64 = base64.b64encode(profile_picture_file.read()).decode()
                    logo_data_url = f"data:{mime_type};base64,{logo_base64}"  # Set dynamic MIME type
            else:
                logo_data_url = None
        else:
            logo_data_url = None

        return logo_data_url
    