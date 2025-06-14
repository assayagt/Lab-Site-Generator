import os
import threading
import uuid
import re

from src.main.DomainLayer.LabWebsites.User.LabMember import LabMember
from src.main.DomainLayer.LabWebsites.User.RegistrationStatus import RegistrationStatus
from src.main.DomainLayer.LabWebsites.User.User import User
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabWebsites.User.Degree import Degree

from src.DAL.DAL_controller import DAL_controller


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
        self.users = {}
        self.members = {}
        self.managers = {}
        self.siteCreator = {}
        self.alumnis = {}
        self.emails_requests_to_register = {}
        self.dal_controller = DAL_controller()
        self._load_data() #=================== LAZY LOAD THAT (?)
        self._initialized = True

    @classmethod
    def get_instance(cls, domain):
        return cls(domain)

    @classmethod
    def reset_instance(cls, domain):
        """Reset the singleton instance for a specific domain."""
        with cls._instance_lock:
            if domain in cls._instances:
                del cls._instances[domain]

    @classmethod
    def reset_all_instances(cls):
        """Reset all UserFacade instances."""
        with cls._instance_lock:
            cls._instances.clear()

    def create_new_site_manager(self, nominated_manager_email, nominated_manager_fullName, nominated_manager_degree):
        if nominated_manager_email in self.members:
            member = self.getLabMemberByEmail(nominated_manager_email)
            del self.members[nominated_manager_email]
        else:
            member = LabMember(nominated_manager_email, nominated_manager_fullName, nominated_manager_degree)
        self.managers[nominated_manager_email] = member
        if nominated_manager_email in self.emails_requests_to_register:
            del self.emails_requests_to_register[nominated_manager_email]
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================
        self.dal_controller.LabMembers_repo.save_to_LabRoles_managers(nominated_manager_email, self.domain)  # ===========================

    def add_email_to_requests(self, email):
        self.emails_requests_to_register[email] = RegistrationStatus.PENDING.value
        self.dal_controller.LabMembers_repo.save_to_emails_pending(email, self.domain, RegistrationStatus.PENDING.value)  # ===========================

    def error_if_email_is_in_requests_and_wait_approval(self, email):
        if email in self.emails_requests_to_register:
            if self.emails_requests_to_register[email] == RegistrationStatus.PENDING.value:
                raise Exception(ExceptionsEnum.REGISTRATION_EMAIL_ALREADY_SENT_TO_MANAGER.value)

    def error_if_email_is_in_requests_and_rejected(self, email):
        if email in self.emails_requests_to_register:
            if self.emails_requests_to_register[email] == RegistrationStatus.REJECTED.value:
                raise Exception(ExceptionsEnum.REGISTRATION_REQUEST_REJECTED_BY_MANAGER.value)

    def getLabMemberByEmail(self, email):
        return self.members[email]

    def error_if_labMember_notExist(self, email):
        if email not in self.members:
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
        member = LabMember(email, fullName, degree)
        self.members[email] = member
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================
        self.dal_controller.LabMembers_repo.save_to_LabRoles_members(member.email, self.domain) # ===========================
        if email in self.emails_requests_to_register:
            del self.emails_requests_to_register[email]

    def approve_registration_request(self, email, fullName, degree):
        if email in self.emails_requests_to_register and self.emails_requests_to_register[email] == RegistrationStatus.PENDING.value:
            self.register_new_LabMember(email, fullName, degree)
        else:
            raise Exception(ExceptionsEnum.DECISION_ALREADY_MADE_FOR_THIS_REGISTRATION_REQUEST.value)

    def reject_registration_request(self, email):
        if email in self.emails_requests_to_register and self.emails_requests_to_register[email] == RegistrationStatus.PENDING.value:
            self.emails_requests_to_register[email] = RegistrationStatus.REJECTED.value
            self.dal_controller.LabMembers_repo.save_to_emails_pending(email, self.domain, RegistrationStatus.REJECTED.value)  # ===========================
        else:
            raise Exception(ExceptionsEnum.DECISION_ALREADY_MADE_FOR_THIS_REGISTRATION_REQUEST.value)

    def getMemberEmailByName(self, author):
        author_lower = author.lower()

        # Search in members
        for email, member in self.members.items():
            if member.fullName and member.fullName.lower() == author_lower:
                return email

        # Search in managers
        for email, manager in self.managers.items():
            if manager.fullName and manager.fullName.lower() == author_lower:
                return email

        # Search in siteCreator
        for email, site_creator in self.siteCreator.items():
            if site_creator.fullName and site_creator.fullName.lower() == author_lower:
                return email

    def get_lab_members_names(self):
        lab_member_names = []
        for email, member in self.members.items():
            lab_member_names.append(member.get_fullName())
        return lab_member_names
    
    def get_lab_members_scholar_links(self):
        res = []
        for member in self.members.values():
            link = member.get_scholarLink()
            if link:
                res.append(link)
        return res

    def get_managers_names(self):
        manager_names = []
        for email, manager in self.managers.items():
            manager_names.append(manager.get_fullName())
        return manager_names
    
    def get_managers_scholar_links(self):
        res = []
        for manager in self.managers.values():
            link = manager.get_scholarLink()
            if link:
                res.append(link)
        return res

    def get_site_creator_name(self):
        creator_names = []
        for email, site_creator in self.siteCreator.items():
            creator_names.append(site_creator.get_fullName())
        return creator_names
    
    def get_site_creator_scholar_links(self):
        res = []
        for site_creator in self.siteCreator.values():
            link = site_creator.get_scholarLink()
            if link:
                res.append(link)
        return res

    def get_alumnis_names(self):
        alumni_names = []
        for email, alumni in self.alumnis.items():
            alumni_names.append(alumni.get_fullName())
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

    def login(self, userId, email):
        """Handle login logic after retrieving user info."""
        user = self.get_user_by_id(userId)
        member = self.get_member_by_email(email)
        if member is not None:
            member.set_user_id(userId)
            user.login(member)

    def logout(self, userId):
        user = self.get_user_by_id(userId)
        user.logout()

    def get_email_by_userId(self, userId):
        user = self.get_user_by_id(userId)
        return user.get_email()

    def error_if_user_not_logged_in(self, userId):
        user = self.get_user_by_id(userId)
        if not user.is_member():
            raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def error_if_user_is_not_manager(self, userId):
        email = self.get_email_by_userId(userId)
        if email not in self.managers:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)

    def error_if_user_is_not_manager_or_site_creator(self, userId):
        email = self.get_email_by_userId(userId)
        if email not in self.managers and email not in self.siteCreator:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER_OR_CREATOR.value)

    def get_member_by_email(self, email) -> LabMember:
        """Retrieve an active Member object by email."""
        if email in self.members:
            return self.members[email]
        elif email in self.managers:
            if email in self.siteCreator:
                return self.siteCreator[email]
            return self.managers[email]
        # todo: verify if alumnis can log in
        # elif email in self.alumnis:
        #    return self.alumnis[email]
        
        return None

    def get_alumni_by_email(self, email):
        if email in self.alumnis:
            return self.alumnis[email]
        return None

    def delete_member_by_email(self, email):
        """Delete an active member by an email
        Site creator cant be deleted!"""
        if email in self.members:
            del self.members[email]
        elif email in self.managers:
            del self.managers[email]

        self.dal_controller.LabMembers_repo.clear_member_role(email, self.domain)  # ===========================

    def get_user_by_id(self, userId) -> User:
        if userId in self.users:
            user = self.users[userId]
        else:
            user = None
        return user

    def error_if_user_notExist(self, userId):
        if self.get_user_by_id(userId) is None:
            raise Exception(ExceptionsEnum.USER_NOT_EXIST.value)

    def verify_if_member_is_manager(self, email):
        if email in self.managers or email in self.siteCreator:
            return True
        return False

    def error_if_member_is_not_labMember_or_manager(self, email):
        if email not in self.members and email not in self.managers:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER.value)

    def error_if_user_is_not_labMember_manager_creator(self, userId):
        email = self.get_email_by_userId(userId)
        if email not in self.members and email not in self.managers and email not in self.siteCreator:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER_OR_CREATOR.value)

    def error_if_user_is_not_labMember_manager_creator_alumni(self, userId):
        email = self.get_email_by_userId(userId)
        if email not in self.members and email not in self.managers and email not in self.siteCreator and email not in self.alumnis:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER_OR_CREATOR_OR_ALUMNI.value)

    def error_if_trying_to_define_site_creator_as_alumni(self, email):
        if email in self.siteCreator:
            raise Exception(ExceptionsEnum.SITE_CREATOR_CANT_BE_ALUMNI.value)

    def define_member_as_alumni(self, email):
        member = self.get_member_by_email(email)
        self.alumnis[email] = member
        self.delete_member_by_email(email)
        self.dal_controller.LabMembers_repo.save_to_LabRoles_alumnis(email, self.domain)  # ===========================

    def get_manager_by_email(self, email):
        return self.managers[email]

    def remove_manager_permissions(self, email):
        if email not in self.managers:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER.value)
        manager = self.get_manager_by_email(email)
        self.members[email] = manager
        del self.managers[email]
        self.dal_controller.LabMembers_repo.save_to_LabRoles_members(email, self.domain)  # ===========================

    def remove_alumni(self, email):
        if email not in self.alumnis:
            raise Exception(ExceptionsEnum.USER_IS_NOT_AN_ALUMNI.value)
        alumni = self.get_alumni_by_email(email)
        self.members[email] = alumni
        del self.alumnis[email]
        self.dal_controller.LabMembers_repo.save_to_LabRoles_members(email, self.domain)  # ===========================

    def getUsers(self):
        return self.users

    def getMembers(self):
        return self.members

    def getManagers(self):
        return self.managers

    def getSiteCreator(self):
        return self.siteCreator

    def getAlumnis(self):
        return self.alumnis

    def set_site_creator(self, creator_email, creator_fullName, creator_degree, creator_scholar_link):
        member = LabMember(creator_email, creator_fullName, creator_degree, scholar_link=creator_scholar_link)
        self.siteCreator[creator_email] = member
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================
        self.dal_controller.LabMembers_repo.save_to_LabRoles_siteCreator(creator_email, self.domain)  # ===========================

    def set_secondEmail_by_member(self, email, secondEmail):
        member = self.get_member_by_email(email)
        if member is None:
            member = self.get_alumni_by_email(email)
        member.set_secondEmail(secondEmail)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================


    def set_linkedin_link_by_member(self, email, linkedin_link):
        member = self.get_member_by_email(email)
        if member is None:
            member = self.get_alumni_by_email(email)
        member.set_linkedin_link(linkedin_link)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================
    
    def set_scholar_link_by_member(self, email, scholar_link):
        member = self.get_member_by_email(email)
        if member is None:
            member = self.get_alumni_by_email(email)
        member.set_scholar_Link(scholar_link)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================

    def set_media_by_member(self, email, media):
        member = self.get_member_by_email(email)
        if member is None:
            member = self.get_alumni_by_email(email)
        member.set_media(media)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================

    def set_fullName_by_member(self,email, fullName):
        member = self.get_member_by_email(email)
        if member is None:
            member = self.get_alumni_by_email(email)
        member.set_fullName(fullName)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================

    def set_degree_by_member(self,email, degree):
        member = self.get_member_by_email(email)
        if member is None:
            member = self.get_alumni_by_email(email)
        member.set_degree(degree)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================

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
            member = self.get_alumni_by_email(email)
        member.set_bio(bio)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))  # ===========================

    def add_user(self):
        user_id = str(uuid.uuid4())
        user = User(user_id=user_id)
        self.users[user_id] = user
        return user_id

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
        # Get all the emails that are in the registration requests list and that their value is RegistrationStatus.PENDING.value
        return [email for email, status in self.emails_requests_to_register.items() if status == RegistrationStatus.PENDING.value]

    def get_all_lab_members_details(self):
        all_members = []
        for email, member in self.members.items():
            all_members.append(member.get_details())
        return all_members

    def get_all_lab_managers_details(self):
        all_managers = []
        for email, member in self.managers.items():
            if email in self.siteCreator.keys():
                all_managers.append(self.get_site_creator_details())
            else:
                all_managers.append(member.get_details())
       
        return all_managers

    def get_site_creator_details(self):
        creator = next(iter(self.siteCreator.values()))  # Get the first (and probably only) creator
        details = creator.get_details()
        print(details)
        details["is_creator"] = True
        return details

    def get_all_alumnis_details(self):
        all_alumnis = []
        for email, member in self.alumnis.items():
            all_alumnis.append(member.get_details())
        return all_alumnis

    def get_user_details(self, email):
        member = self.get_member_by_email(email)
        return member.get_details()

    def resign_site_creator(self, new_role):
        if new_role == "alumni":
            self.site_creator_to_alumni()
        if new_role == "manager":
            self.site_creator_to_manager()
        elif new_role == "member":
            self.site_creator_to_member()

    def site_creator_to_alumni(self):
        site_creator_email, site_creator = next(iter(self.siteCreator.items()))
        self.alumnis[site_creator_email] = site_creator
        del self.siteCreator[site_creator_email]
        self.dal_controller.LabMembers_repo.save_to_LabRoles_alumnis(site_creator_email, self.domain)

    def site_creator_to_manager(self):
        site_creator_email, site_creator = next(iter(self.siteCreator.items()))
        self.managers[site_creator_email] = site_creator
        del self.siteCreator[site_creator_email]
        self.dal_controller.LabMembers_repo.save_to_LabRoles_managers(site_creator_email, self.domain)

    def site_creator_to_member(self):
        site_creator_email, site_creator = next(iter(self.siteCreator.items()))
        self.members[site_creator_email] = site_creator
        del self.siteCreator[site_creator_email]
        self.dal_controller.LabMembers_repo.save_to_LabRoles_members(site_creator_email, self.domain)

    def define_member_as_site_creator(self, nominate_email):
        member = self.get_member_by_email(nominate_email)
        self.siteCreator[nominate_email] = member
        del self.members[nominate_email]
        self.dal_controller.LabMembers_repo.save_to_LabRoles_siteCreator(nominate_email, self.domain)

    def get_fullName_by_email(self, email):
        """
        Get the full name of a member by their email.
        """
        if email in self.members:
            return self.members[email].get_fullName()
        elif email in self.managers:
            return self.managers[email].get_fullName()
        elif email in self.siteCreator:
            return self.siteCreator[email].get_fullName()
    
    def get_scholar_link_by_email(self, email):
        """
            Get Google Scholar profile link of member by email.
        """
        if email in self.members:
            return self.members[email].get_scholarLink()
        elif email in self.managers:
            return self.managers[email].get_scholarLink()
        elif email in self.siteCreator:
            return self.siteCreator[email].get_scholarLink()
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
                email_notifications=dto.email_notifications
            )
    
##TODO: there is an error doesnt load all the fields!!!!!!
    def _load_data(self):
        repo = self.dal_controller.LabMembers_repo

        # Load members
        for dto in repo.find_all_members_by_domain(self.domain):
           self.members[dto.email] = self._LabMember_dto_to_Object(dto)

        # Load managers
        for dto in repo.find_all_managers_by_domain(self.domain):
            self.managers[dto.email] = self._LabMember_dto_to_Object(dto)

        # Load site creators (and also treat them as a manager)
        for dto in repo.find_all_siteCreators_by_domain(self.domain):
            lm = self._LabMember_dto_to_Object(dto)
            self.siteCreator[dto.email] = lm
            self.managers[dto.email] = lm

        # Load alumnis
        for dto in repo.find_all_alumnis_by_domain(self.domain):
            self.alumnis[dto.email] = self._LabMember_dto_to_Object(dto)

        # Load pending registration emails
        for email in repo.find_all_pending_emails_by_domain(self.domain):
            self.emails_requests_to_register[email] = RegistrationStatus.PENDING.value
        # Debug output (optional)
        print(f"Loaded UserFacade for domain={self.domain}: "
              f"{len(self.members)} members, "
              f"{len(self.managers)} managers, "
              f"{len(self.siteCreator)} creators, "
              f"{len(self.alumnis)} alumnis, "
              f"{len(self.emails_requests_to_register)} pending requests")

    def add_profile_picture(self, user_id, file_path):
        user = self.get_user_by_id(user_id)
        if user is None:
            raise Exception(ExceptionsEnum.USER_NOT_EXIST.value)
        member = self.get_member_by_email(user.get_email())
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

    def set_email_notifications(self, user_id, email_notifications):
        user = self.get_user_by_id(user_id)
        if user is None:
            raise Exception(ExceptionsEnum.USER_NOT_EXIST.value)
        member = self.get_member_by_email(user.get_email())
        if member is None:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)
        member.set_email_notifications(email_notifications)
        self.dal_controller.LabMembers_repo.save_LabMember(member.get_dto(self.domain))

    def get_email_notifications(self, email):
        member = self.get_member_by_email(email)
        if member is None:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_LAB_MEMBER.value)
        return member.get_email_notifications()

        
