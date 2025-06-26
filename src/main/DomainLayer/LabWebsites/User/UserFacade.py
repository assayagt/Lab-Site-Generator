import os
import threading
import uuid
import re

from src.main.DomainLayer.LabWebsites.User.LabMember import LabMember
from src.main.DomainLayer.LabWebsites.User.RegistrationStatus import RegistrationStatus
from src.main.DomainLayer.LabWebsites.User.User import User
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabWebsites.User.Role import Role
from src.main.DomainLayer.LabWebsites.User.Degree import Degree
from src.DAL.DAL_controller import DAL_controller
from src.main.DomainLayer.LabWebsites.User.Role import Role
from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = "894370088866-4jkvg622sluvf0k7cfv737tnjlgg00nt.apps.googleusercontent.com"

class UserFacade:
    _instances = {}  # map: domain -> instance
    _instance_lock = threading.Lock()

    def __new__(cls, domain):
        with cls._instance_lock:
            if domain not in cls._instances:
                instance = super(UserFacade, cls).__new__(cls)
                instance._initialized = False
                cls._instances[domain] = instance
        return cls._instances[domain]

    def __init__(self, domain):
        if self._initialized:
            return
        self.domain = domain
        self.dal_controller = DAL_controller()
        self._initialized = True

    @classmethod
    def get_instance(cls, domain):
        return cls(domain)

    @classmethod
    def reset_instance(cls, domain):
        with cls._instance_lock:
            if domain in cls._instances:
                del cls._instances[domain]

    @classmethod
    def reset_all_instances(cls):
        """Reset all UserFacade instances."""
        with cls._instance_lock:
            cls._instances.clear()

    def get_member_by_email(self, email):
        dto = self.dal_controller.LabMembers_repo.find_LabMember_by_domain_email(self.domain, email)
        if dto:
            return self._LabMember_dto_to_Object(dto)
        return None

    def create_new_site_manager(self, nominated_manager_email, nominated_manager_fullName, nominated_manager_degree):
        member = self.get_member_by_email(nominated_manager_email)
        if not member:
            member = LabMember(nominated_manager_email, nominated_manager_fullName, nominated_manager_degree)
        member.set_role(Role.MANAGER)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))
        self.dal_controller.LabMembers_repo.delete_from_emails_pending(nominated_manager_email, self.domain)

    def add_email_to_requests(self, email):
        self.dal_controller.LabMembers_repo.save_to_emails_pending(email, self.domain, RegistrationStatus.PENDING.value)

    def get_registration_status(self, email):
        # get status of email by domain and email
        return self.dal_controller.LabMembers_repo.get_status_of_email_by_domain_email(self.domain, email)

    def error_if_email_is_in_requests_and_wait_approval(self, email):
        status = self.get_registration_status(email)
        if status == RegistrationStatus.PENDING.value:
            raise Exception(ExceptionsEnum.REGISTRATION_EMAIL_ALREADY_SENT_TO_MANAGER.value)

    def error_if_email_is_in_requests_and_rejected(self, email):
        status = self.get_registration_status(email)
        if status == RegistrationStatus.REJECTED.value:
            raise Exception(ExceptionsEnum.REGISTRATION_REQUEST_REJECTED_BY_MANAGER.value)

    def error_if_labMember_notExist(self, email):
        member = self.get_member_by_email(email)
        if not member:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)

    def error_if_email_is_not_valid(self, email):
        """
        Validate the email format using a regular expression.
        Raise an error if the email is not valid.
        """
        email_regex = (
            r"^(?!.*\.\.)(?!.*\.$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
        if re.match(email_regex, email) is None:
            raise Exception(ExceptionsEnum.INVALID_EMAIL_FORMAT.value)

    def register_new_LabMember(self, email, fullName, degree):
        member = self.get_member_by_email(email)
        if member is not None:
            raise Exception(ExceptionsEnum.EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_MEMBER.value)
        member = LabMember(email, fullName, degree, role=Role.MEMBER)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))
        self.dal_controller.LabMembers_repo.delete_from_emails_pending(email, self.domain)

    def approve_registration_request(self, email, fullName, degree):
        status = self.get_registration_status(email)
        if status == RegistrationStatus.PENDING.value:
            self.register_new_LabMember(email, fullName, degree)
        else:
            raise Exception(ExceptionsEnum.DECISION_ALREADY_MADE_FOR_THIS_REGISTRATION_REQUEST.value)

    def reject_registration_request(self, email):
        status = self.get_registration_status(email)
        if status == RegistrationStatus.PENDING.value:
            self.dal_controller.LabMembers_repo.save_to_emails_pending(email, self.domain, RegistrationStatus.REJECTED.value)
        else:
            raise Exception(ExceptionsEnum.DECISION_ALREADY_MADE_FOR_THIS_REGISTRATION_REQUEST.value)

    def getMemberEmailByName(self, author):
        author_lower = author.lower()

        # use find all by domain and then filter by fullName
        for dto in self.dal_controller.LabMembers_repo.find_all_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            if member.fullName and member.fullName.lower() == author_lower:
                return member.email
        return None

    def get_lab_members_names(self):
        lab_member_names = []
        for dto in self.dal_controller.LabMembers_repo.find_all_lab_members_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            lab_member_names.append(member.get_fullName())
        return lab_member_names

    def get_lab_members_scholar_links(self):
        res = []
        for dto in self.dal_controller.LabMembers_repo.find_all_lab_members_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            link = member.get_scholarLink()
            if link:
                res.append(link)
        return res

    def get_managers_names(self):
        manager_names = []
        for dto in self.dal_controller.LabMembers_repo.find_all_managers_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            manager_names.append(member.get_fullName())
        return manager_names

    def get_managers_scholar_links(self):
        res = []
        for dto in self.dal_controller.LabMembers_repo.find_all_managers_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            link = member.get_scholarLink()
            if link:
                res.append(link)
        return res

    def get_site_creator_name(self):
        creator_names = []
        for dto in self.dal_controller.LabMembers_repo.find_all_siteCreators_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            creator_names.append(member.get_fullName())
        return creator_names

    def get_site_creator_scholar_links(self):
        res = []
        for dto in self.dal_controller.LabMembers_repo.find_all_siteCreators_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            link = member.get_scholarLink()
            if link:
                res.append(link)
        return res

    def get_alumnis_names(self):
        alumni_names = []
        for dto in self.dal_controller.LabMembers_repo.find_all_alumnis_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            alumni_names.append(member.get_fullName())
        return alumni_names

    def get_all_members_names(self):
        member_names = []
        member_names.extend(self.get_active_members_names())
        member_names.extend(self.get_alumnis_names())
        return member_names

    def get_active_members_names(self):
        member_names = []
        member_names.extend(self.get_lab_members_names())
        member_names.extend(self.get_managers_names())
        member_names.extend(self.get_site_creator_name())
        return member_names

    def get_active_members_scholar_links(self):
        member_scholarIds = []
        member_scholarIds.extend(self.get_lab_members_scholar_links())
        member_scholarIds.extend(self.get_managers_scholar_links())
        member_scholarIds.extend(self.get_site_creator_scholar_links())
        return member_scholarIds

    def define_member_as_alumni(self, email):
        member = self.get_member_by_email(email)
        if member:
            member.set_role(Role.ALUMNI)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def remove_manager_permissions(self, email):
        member = self.get_member_by_email(email)
        if not member or member.get_role() != Role.MANAGER:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)
        member.set_role(Role.MEMBER)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def remove_alumni(self, email):
        member = self.get_member_by_email(email)
        if not member or member.get_role() != Role.ALUMNI:
            raise Exception(ExceptionsEnum.USER_IS_NOT_AN_ALUMNI.value)
        member.set_role(Role.MEMBER)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def delete_member_by_email(self, email):
        self.dal_controller.LabMembers_repo.delete_LabMember(email, self.domain)

    def set_site_creator(self, creator_email, creator_fullName, creator_degree, creator_scholar_link):
        member = LabMember(creator_email, creator_fullName, creator_degree, scholar_link=creator_scholar_link, role=Role.CREATOR)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def set_secondEmail_by_member(self, email, secondEmail):
        member = self.get_member_by_email(email)
        if member:
            member.set_secondEmail(secondEmail)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def set_linkedin_link_by_member(self, email, linkedin_link):
        member = self.get_member_by_email(email)
        if member:
            member.set_linkedin_link(linkedin_link)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def set_scholar_link_by_member(self, email, scholar_link):
        member = self.get_member_by_email(email)
        if member:
            member.set_scholar_Link(scholar_link)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def set_media_by_member(self, email, media):
        member = self.get_member_by_email(email)
        if member:
            member.set_media(media)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def set_fullName_by_member(self, email, fullName):
        member = self.get_member_by_email(email)
        if member:
            member.set_fullName(fullName)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def set_degree_by_member(self, email, degree):
        member = self.get_member_by_email(email)
        if member:
            member.set_degree(degree)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def error_if_degree_not_valid(self, degree):
        print(degree)
        if isinstance(degree, str):
            valid_degrees = {d.value for d in Degree}
            print(valid_degrees)
            if degree not in valid_degrees:
                raise Exception(ExceptionsEnum.INVALID_DEGREE.value)
        elif isinstance(degree, Degree):
            if degree not in Degree:
                raise Exception(ExceptionsEnum.INVALID_DEGREE.value)
        else:
            raise Exception(ExceptionsEnum.INVALID_DEGREE.value)

    def set_bio_by_member(self,email, bio):
        member = self.get_member_by_email(email)
        if member is None:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)
        member.set_bio(bio)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def error_if_linkedin_link_not_valid(self, linkedin_link):
        """
        Validates if the given LinkedIn link is in the correct format.
        """
        # Define a regex pattern for valid LinkedIn profile URLs
        linkedin_pattern = re.compile(
            r"^https://(www\.)?linkedin\.com/in/[\w\-]+/?$"
        )
        if not linkedin_pattern.match(linkedin_link):
            raise ValueError(ExceptionsEnum.INVALID_LINKEDIN_LINK.value)
        
    def error_if_scholar_link_not_valid(self, scholar_link):
        """
        Validates if the given Google Scholar link is strictly a profile link.
        """
        # Strict regex for valid Google Scholar profile URLs only
        scholar_pattern = re.compile(
           r"^https://(www\.)?scholar\.google\.com/citations\?user=[a-zA-Z0-9_-]{5,}(&[a-zA-Z0-9=_-]+)*$"

        )
        if not scholar_pattern.match(scholar_link):
            raise ValueError(ExceptionsEnum.INVALID_SCHOLAR_LINK.value)

    def get_pending_registration_emails(self):
        return self.dal_controller.LabMembers_repo.find_all_pending_emails_by_domain(self.domain)

    def get_all_lab_members_details(self):
        all_members = []
        for dto in self.dal_controller.LabMembers_repo.find_all_lab_members_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            all_members.append(member.get_details())
        return all_members

    def get_all_lab_managers_details(self):
        #include site creator
        site_creator = self.get_site_creator_details()
        all_managers = []
        for dto in self.dal_controller.LabMembers_repo.find_all_managers_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            all_managers.append(member.get_details())
        if site_creator:
            all_managers.append(site_creator)
        return all_managers

    def get_site_creator_details(self):
        for dto in self.dal_controller.LabMembers_repo.find_all_siteCreators_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            return member.get_details()
        return None

    def get_all_alumnis_details(self):
        all_alumnis = []
        for dto in self.dal_controller.LabMembers_repo.find_all_alumnis_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            all_alumnis.append(member.get_details())
        return all_alumnis

    def get_user_details(self, email):
        member = self.get_member_by_email(email)
        if member:
            return member.get_details()
        return None

    def resign_site_creator(self, new_role):
        if new_role == "alumni":
            self.site_creator_to_alumni()
        if new_role == "manager":
            self.site_creator_to_manager()
        elif new_role == "member":
            self.site_creator_to_member()

    def site_creator_to_alumni(self):
        for dto in self.dal_controller.LabMembers_repo.find_all_siteCreators_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            if member.get_role() == Role.CREATOR:
                member.set_role(Role.ALUMNI)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))
            break

    def site_creator_to_manager(self):
        for dto in self.dal_controller.LabMembers_repo.find_all_siteCreators_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            if member.get_role() == Role.CREATOR:
                member.set_role(Role.MANAGER)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))
            break

    def site_creator_to_member(self):
        for dto in self.dal_controller.LabMembers_repo.find_all_siteCreators_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            if member.get_role() == Role.CREATOR:
                member.set_role(Role.MEMBER)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))
            break

    def define_member_as_site_creator(self, nominate_email):
        member = self.get_member_by_email(nominate_email)
        if member:
            member.set_role(Role.CREATOR)
            self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def get_fullName_by_email(self, email):
        member = self.get_member_by_email(email)
        if member:
            return member.get_fullName()
        return None

    def get_scholar_link_by_email(self, email):
        member = self.get_member_by_email(email)
        if member:
            return member.get_scholarLink()
        return None

    def _LabMember_dto_to_Object(self, dto):
        return LabMember(
                email=dto.email,
                fullName=dto.full_name,
                degree=dto.degree,
                secondEmail=dto.second_email,
                linkedin_link=dto.linkedin_link,
                media=dto.media,
                user_id=None,
                bio=dto.bio,
                scholar_link=dto.scholar_link,
                profile_picture=dto.profile_picture,
                email_notifications=dto.email_notifications,
                role=dto.role
            )
    
    def add_profile_picture(self, email, file_path):
        member = self.get_member_by_email(email)
        if member is None:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)
        curr_picture = member.get_profile_picture()
        if curr_picture is not None:
            # remove the old profile picture
            self.remove_profile_picture(curr_picture)

        member.set_profile_picture(file_path)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def remove_profile_picture(self, curr_picture):
        if os.path.exists(curr_picture):
            os.remove(curr_picture)
        else:
            raise Exception(ExceptionsEnum.IMAGE_NOT_FOUND.value)

    def set_email_notifications(self, email, email_notifications):
        member = self.get_member_by_email(email)
        if member is None:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)
        member.set_email_notifications(email_notifications)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def get_email_notifications(self, email):
        member = self.get_member_by_email(email)
        if member is None:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)
        return member.get_email_notifications()

    def error_if_user_not_logged_in(self, userId):
        try:
            email = self.get_email_from_token(google_token=userId)
            if not self.get_member_by_email(email):
                raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER.value)
        except Exception as e:
            raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER.value)
    
    def error_if_user_is_not_manager_or_site_creator(self, userId):
        member = self.get_member_by_email(userId)
        if member and member.get_role() != Role.MANAGER and member.get_role() != Role.CREATOR:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)
    
    def error_if_trying_to_define_site_creator_as_alumni(self, email):
        member = self.get_member_by_email(email)
        if member and member.get_role() == Role.CREATOR:
            raise Exception(ExceptionsEnum.SITE_CREATOR_CANT_BE_ALUMNI.value)
        
    def error_if_member_is_not_labMember_or_manager(self, email):
        member = self.get_member_by_email(email)
        if member and member.get_role() != Role.MEMBER and member.get_role() != Role.MANAGER:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)

    def get_email_from_token(self, google_token):
        # Verify the token
        try:
            idinfo = id_token.verify_oauth2_token(
            google_token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=2,
            )

            return idinfo["email"]
        except Exception as e:
            raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER.value)
        
    def error_if_user_is_not_site_creator(self, email):
        member = self.get_member_by_email(email)
        if member and member.get_role() != Role.CREATOR:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def verify_if_member_is_manager(self, email):
        # get all managers and site creators from db and check if email is in the list
        member = self.get_member_by_email(email)
        if member and (member.get_role() == Role.MANAGER or member.get_role() == Role.CREATOR):
            return True
        return False

    def get_managers_emails(self):
        managers_emails = []
        for dto in self.dal_controller.LabMembers_repo.find_all_managers_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            managers_emails.append(member.get_email())
        return managers_emails
    
    def get_site_creator_emails(self):
        site_creator_emails = []
        for dto in self.dal_controller.LabMembers_repo.find_all_siteCreators_by_domain(self.domain):
            member = self._LabMember_dto_to_Object(dto)
            site_creator_emails.append(member.get_email())
        return site_creator_emails

    def error_if_user_notExist(self, email):
        pass

    def error_if_user_is_not_labMember_manager_creator(self, email):
        member = self.get_member_by_email(email)
        if member and member.get_role() != Role.MEMBER and member.get_role() != Role.MANAGER and member.get_role() != Role.CREATOR:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)