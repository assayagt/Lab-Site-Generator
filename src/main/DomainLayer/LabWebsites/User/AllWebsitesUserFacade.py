from src.main.DomainLayer.LabWebsites.User.UserFacade import UserFacade
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.DAL.DAL_controller import DAL_controller

import threading, json

class AllWebsitesUserFacade:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(AllWebsitesUserFacade, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.usersFacades = {}  # key: website domain, value: userFacade
        self.dal_controller = DAL_controller()
        # self._load_all_data()
        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance. Useful for unit tests."""
        with cls._instance_lock:
            cls._instance = None

    # def add_new_webstie_userFacade(self, domain):
    #     self.usersFacades[domain] = UserFacade.get_instance(domain) ==> Lazy-load mechanism covers that 

    def getUserFacadeByDomain(self, domain) -> UserFacade:
        # first, verify this domain exists in the website table
        if self.dal_controller.website_repo.find_by_domain(domain) is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)
        
        # lazy-create the userFacade
        if domain not in self.usersFacades:
            # this calls UserFacade.__init__ and its _load_data()
            self.usersFacades[domain] = UserFacade.get_instance(domain)
        return self.usersFacades[domain]

    def error_if_domain_not_exist(self, domain):
        if domain not in self.usersFacades:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

    def logout(self, domain, userId):
        self.error_if_domain_not_exist(domain)
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.logout(userId)

    def approve_registration_request(self, domain, manager_userId, requested_email, requested_full_name, requested_degree):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(manager_userId)
        userFacade.approve_registration_request(requested_email, requested_full_name, requested_degree)

    def reject_registration_request(self, domain, manager_userId, requested_email):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(manager_userId)
        userFacade.reject_registration_request(requested_email)

    def create_new_site_manager_from_labWebsite(self, nominator_manager_userId, nominated_manager_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(nominator_manager_userId)
        userFacade.error_if_user_not_logged_in(nominator_manager_userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(nominator_manager_userId)
        userFacade.error_if_labMember_notExist(nominated_manager_email)
        nominated_manager_fullName = userFacade.getLabMemberByEmail(nominated_manager_email).get_fullName()
        nominated_manager_degree = userFacade.getLabMemberByEmail(nominated_manager_email).get_degree()
        userFacade.create_new_site_manager(nominated_manager_email, nominated_manager_fullName, nominated_manager_degree)

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(manager_userId)
        userFacade.error_if_email_is_not_valid(email_to_register)
        userFacade.error_if_degree_not_valid(lab_member_degree)
        userFacade.register_new_LabMember(email_to_register, lab_member_fullName, lab_member_degree)

    def create_new_site_manager_from_generator(self, nominated_manager_email, domain):
        self.error_if_domain_not_exist(domain)
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_labMember_notExist(nominated_manager_email)
        nominated_manager_fullName = userFacade.getLabMemberByEmail(nominated_manager_email).get_fullName()
        nominated_manager_degree = userFacade.getLabMemberByEmail(nominated_manager_email).get_degree()
        userFacade.create_new_site_manager(nominated_manager_email, nominated_manager_fullName, nominated_manager_degree)

    def register_new_LabMember_from_generator(self, email_to_register, lab_member_fullName, lab_member_degree, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_email_is_not_valid(email_to_register)
        userFacade.error_if_degree_not_valid(lab_member_degree)
        userFacade.register_new_LabMember(email_to_register, lab_member_fullName, lab_member_degree)

    def define_member_as_alumni_from_generator(self, member_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_trying_to_define_site_creator_as_alumni(member_email)
        userFacade.error_if_member_is_not_labMember_or_manager(member_email)
        userFacade.define_member_as_alumni(member_email)

    def define_member_as_alumni(self, manager_userId, member_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(manager_userId)
        userFacade.error_if_trying_to_define_site_creator_as_alumni(member_email)
        userFacade.error_if_member_is_not_labMember_or_manager(member_email)
        userFacade.define_member_as_alumni(member_email)

    def remove_manager_permission(self, manager_userId, manager_toRemove_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(manager_userId)
        userFacade.remove_manager_permissions(manager_toRemove_email)

    def getMemberEmailByName(self, author, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.getMemberEmailByName(author)

    def get_all_alumnis(self, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.getAlumnis()

    def get_all_lab_members(self, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.getMembers()

    def get_all_lab_managers(self, domain):
        """notice! this function returns all managers including site creator!"""
        userFacade = self.getUserFacadeByDomain(domain)
        managers = userFacade.getManagers()
        siteCreator = userFacade.getSiteCreator()
        return {**managers, **siteCreator}

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator_alumni(userid)
        userFacade.error_if_email_is_not_valid(secondEmail)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_secondEmail_by_member(email, secondEmail)

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator_alumni(userid)
        userFacade.error_if_linkedin_link_not_valid(linkedin_link)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_linkedin_link_by_member(email, linkedin_link)

    def set_scholar_link_by_member(self, userid, scholar_link, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator_alumni(userid)
        userFacade.error_if_scholar_link_not_valid(scholar_link)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_scholar_link_by_member(email, scholar_link)

    def set_media_by_member(self, userid, media, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator_alumni(userid)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_media_by_member(email, media)

    def set_fullName_by_member(self, userid, fullName, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator_alumni(userid)
        if not fullName:
            raise Exception(ExceptionsEnum.INVALID_FULL_NAME.value)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_fullName_by_member(email, fullName)

    def set_degree_by_member(self, userid, degree, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator_alumni(userid)
        userFacade.error_if_degree_not_valid(degree)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_degree_by_member(email, degree)

    def set_bio_by_member(self, userid, bio, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator_alumni(userid)
        email = userFacade.get_email_by_userId(userid)
        userFacade.set_bio_by_member(email, bio)

    def add_user_to_website(self, domain):
        return self.getUserFacadeByDomain(domain).add_user()

    def get_active_members_names(self, domain):
        return self.getUserFacadeByDomain(domain).get_active_members_names()
    
    def get_active_members_scholarLinks(self, domain):
        return self.getUserFacadeByDomain(domain=domain).get_active_members_scholar_links()

    def get_all_members_names(self, domain):
        '''returns all lab members + managers + site creator + alumnis names'''
        return self.getUserFacadeByDomain(domain).get_all_members_names()

    def get_pending_registration_emails(self, domain):
        return self.getUserFacadeByDomain(domain).get_pending_registration_emails()

    def get_all_lab_members_details(self, domain):
        return self.getUserFacadeByDomain(domain).get_all_lab_members_details()

    def get_all_lab_managers_details(self, domain):
        return self.getUserFacadeByDomain(domain).get_all_lab_managers_details()

    def get_all_alumnis_details(self, domain):
        return self.getUserFacadeByDomain(domain).get_all_alumnis_details()

    def get_user_details(self, userid, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        userFacade.error_if_user_is_not_labMember_manager_creator(userid)
        email = userFacade.get_email_by_userId(userid)
        return userFacade.get_user_details(email)

    def site_creator_resignation_from_lab_website(self, site_creator_user_id, domain, nominate_email, new_role):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(site_creator_user_id)
        userFacade.error_if_user_not_logged_in(site_creator_user_id)
        userFacade.error_if_user_is_not_site_creator(site_creator_user_id)

        # Resign the site creator from its role
        userFacade.resign_site_creator(new_role)

        # Assign nominated as site creator
        userFacade.error_if_member_is_not_labMember_or_manager(nominate_email)
        userFacade.define_member_as_site_creator(nominate_email)

    def site_creator_resignation_from_generator(self, domain, nominate_email, new_role):
        userFacade = self.getUserFacadeByDomain(domain)

        # Resign the site creator from its role
        userFacade.resign_site_creator(new_role)

        # Assign nominated as site creator
        userFacade.error_if_member_is_not_labMember_or_manager(nominate_email)
        userFacade.define_member_as_site_creator(nominate_email)

    def _load_all_data(self):
        """
        Load all websites from the repository and create UserFacades for each.
        Args:
            website_repo (WebsiteRepository): The repository to fetch websites from.
        """
    
        websites = self.dal_controller.website_repo.find_all()
 
        if websites:
            for website in websites:
                domain = website.domain
                if domain not in self.usersFacades:
                    self.usersFacades[domain] = UserFacade(domain)

    def reset_system(self):
        """
        Resets the entire system by clearing all stored websites.
        """
        self.usersFacades.clear()
        self.dal_controller.drop_all_tables()

    def get_fullName_by_email(self, nominated_manager_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        return userFacade.get_fullName_by_email(nominated_manager_email)

    def remove_alumni_from_labWebsite(self, manager_userId, alumni_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(manager_userId)
        userFacade.remove_alumni(alumni_email)

    def remove_website_data(self, domain):
        """
        Remove all data associated with a website from memory and database.

        Args:
            domain (str): The domain of the website to remove
        """
        if domain in self.usersFacades:
            # Get all members before removing the facade
            user_facade = self.usersFacades[domain]

            # Reset the singleton instance
            user_facade.reset_instance(domain)

            # Remove from memory
            del self.usersFacades[domain]

    def remove_alumni_from_labWebsite(self, manager_userId, alumni_email, domain):
        userFacade = self.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(manager_userId)
        userFacade.error_if_user_not_logged_in(manager_userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(manager_userId)
        userFacade.remove_alumni(alumni_email)
    
    def get_scholar_link_by_email(self, email, domain):
        return self.getUserFacadeByDomain(domain).get_scholar_link_by_email(email)
