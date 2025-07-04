import os
import re
import threading

from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustomFacade import SiteCustomFacade, Template
from src.main.DomainLayer.LabGenerator.User.UserFacade import UserFacade
from src.main.DomainLayer.LabWebsites.LabSystem.LabSystemController import LabSystemController
from src.main.Util.ExceptionsEnum import ExceptionsEnum


class GeneratorSystemController:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(GeneratorSystemController, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Initialize only once
        self.user_facade = UserFacade()
        self.site_custom_facade = SiteCustomFacade()
        self.labSystem = LabSystemController()

        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance. Safe to use in unit tests."""
        with cls._instance_lock:
            cls._instance = None

    def get_lab_system_controller(self):
        """Get the lab system controller."""
        return self.labSystem

    def create_website(self, user_id, website_name, domain, components, template):
        """Create a website using SiteCustomFacade."""
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.error_if_domain_already_exist(domain)
        email = self.user_facade.get_email_from_token(user_id)
        self.site_custom_facade.create_new_site(domain, website_name, components, template, email)
        self.user_facade.create_new_site_manager(email, domain)

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator, creator_scholar_link):
        """
        Generates a new lab website once the custom site configuration is complete.
        Parameters:
        domain (str): The domain of the new lab website.
        lab_members (dict): A dictionary of lab members where each key is the email,
                            and the value is another dictionary containing "full_name" and "degree".
        lab_managers (dict): A dictionary of lab managers where each key is the email,
                             and the value is another dictionary containing "full_name" and "degree".
        site_creator (dict): A dictionary containing "email", "full_name", and "degree" of the site creator.
        """
        self.site_custom_facade.error_if_domain_not_exist(domain)
        self.site_custom_facade.set_custom_site_as_generated(domain)
        lab_managers_emails = list(lab_managers.keys())
        self.user_facade.create_new_site_managers(lab_managers_emails, domain)
        self.labSystem.create_new_lab_website(domain, lab_members, lab_managers, site_creator, creator_scholar_link)
        self.set_site_logo_on_site_creation(domain)
        self.set_site_home_picture_on_site_creation(domain)

    def set_site_about_us_on_creation_from_generator(self, domain, about_us):
        """
        Set the about us section on lab website creation. This function should be called after create_new_lab_website.
        """
        self.labSystem.set_site_about_us_from_generator(domain, about_us)

    def get_site_about_us_from_generator(self, domain):
        """
        Get the about us section
        """
        if self.site_custom_facade.get_if_site_is_generated(domain=domain):
            return self.labSystem.get_about_us(domain)
        return ""

    def set_site_about_us_by_manager_from_generator(self, user_id, domain, about_us):
        """
        Set the about us section by manager
        """
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        self.set_site_about_us_on_creation_from_generator(domain, about_us)

    def set_site_contact_info_on_creation_from_generator(self, domain, contact_info_dto):
        """
        Set the contact us section on lab website creation. This function should be called after create_new_lab_website.
        """
        if not re.match(r"^\+?[0-9\s\-()]+$", contact_info_dto.lab_phone_num):
            raise Exception(ExceptionsEnum.INVALID_PHONE_NUMBER.value)
        self.labSystem.set_site_contact_info_from_generator(domain, contact_info_dto)

    def get_contact_info_from_generator(self, domain):
        """
        Get the contact us section
        """
        if self.site_custom_facade.get_if_site_is_generated(domain=domain):
            return self.labSystem.get_contact_us(domain)
        return ""

    def set_site_contact_info_by_manager_from_generator(self, user_id, domain, contact_info_dto):
        """
        Set the contact us section by manager
        """
        if not re.match(r"^\+?[0-9\s\-()]+$", contact_info_dto.lab_phone_num):
            raise Exception(ExceptionsEnum.INVALID_PHONE_NUMBER.value)
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        self.set_site_contact_info_on_creation_from_generator(domain, contact_info_dto)

    def set_site_logo_on_site_creation(self, domain):
        """
        Set the site logo on lab website creation.
        """
        self.site_custom_facade.error_if_domain_not_exist(domain)

        # Get the logo extension if it's available
        logo_extensions = ['.svg', '.png', '.jpg', '.jpeg']  # Supported logo formats
        logo_path = None
        
        # Loop through possible logo extensions
        for ext in logo_extensions:
            possible_path = os.path.join('./LabWebsitesUploads', domain, f"logo{ext}")
            if os.path.exists(possible_path):
                logo_path = possible_path  # Set the correct logo path if it exists
                break  # Stop as soon as a matching file is found
        logo = None
        if logo_path and os.path.exists(logo_path):
            logo = logo_path
        self.site_custom_facade.set_logo(domain, logo)

    def change_site_logo_by_manager(self, user_id, domain):
        """
        Change the site logo by the manager.
        """
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.error_if_domain_not_exist(domain)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        self.set_site_logo_on_site_creation(domain)

    def set_site_home_picture_on_site_creation(self, domain):
        """
        Set the site home picture on lab website creation.
        """
        self.site_custom_facade.error_if_domain_not_exist(domain)

        logo_extensions = ['.svg', '.png', '.jpg', '.jpeg']  # Supported logo formats
        home_picture_path = None
        
        # Loop through possible logo extensions
        for ext in logo_extensions:
            possible_path = os.path.join('./LabWebsitesUploads', domain, f"homepagephoto{ext}")
            if os.path.exists(possible_path):
                home_picture_path = possible_path  # Set the correct logo path if it exists
                break  # Stop as soon as a matching file is found
        home_picture = None
        if home_picture_path and os.path.exists(home_picture_path):
            home_picture = home_picture_path
        self.site_custom_facade.set_home_picture(domain, home_picture)

    def change_site_home_picture_by_manager(self, user_id, domain):
        """
        Change the site home picture by the manager.
        """
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        self.set_site_home_picture_on_site_creation(domain)

    def change_website_name(self, user_id, new_name, domain):
        """Change website details using SiteCustomFacade."""
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.error_if_domain_not_exist(domain)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        self.site_custom_facade.change_site_name(domain, new_name)

    def change_website_domain(self, user_id, new_domain, domain):
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.error_if_domain_not_exist(domain)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        self.site_custom_facade.error_if_domain_is_not_valid(new_domain)
        self.site_custom_facade.error_if_domain_already_exist(new_domain)
        self.site_custom_facade.change_site_domain(domain, new_domain)
        self.user_facade.change_site_domain(domain, new_domain)
    
    def change_website_template(self, user_id, domain, new_template = Template):
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.error_if_domain_not_exist(domain)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        self.site_custom_facade.change_site_template(domain, new_template)

    def add_components_to_site(self, user_id, domain, new_components):
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.error_if_domain_not_exist(domain)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        self.site_custom_facade.add_components_to_site(domain, new_components)

    def create_new_site_manager(self, nominator_manager_userId, nominated_manager_email, domain):
        """
        Define and add new manager to a specific website, from generator site.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        """
        self.user_facade.error_if_user_notExist(nominator_manager_userId)
        self.user_facade.error_if_user_not_logged_in(nominator_manager_userId)
        self.user_facade.error_if_user_is_not_site_manager(nominator_manager_userId, domain)
        self.user_facade.create_new_site_manager(nominated_manager_email, domain)
        self.labSystem.create_new_site_manager_from_generator(domain, nominated_manager_email)

    def create_new_site_manager_from_lab_website(self, nominated_manager_email, domain):
        """
        Define and add new manager to a specific website, from lab website.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        """
        self.user_facade.create_new_site_manager(nominated_manager_email, domain)

    def add_alumni_from_generator(self, manager_userId, email_toSetAlumni, domain):
        """
        Define a lab member or lab manager as alumni in a specific website, from generator site.
        The given email_toSetAlumni must be associated with a Lab Member of the given website.
        """
        self.user_facade.error_if_user_notExist(manager_userId)
        self.user_facade.error_if_user_not_logged_in(manager_userId)
        self.user_facade.error_if_user_is_not_site_manager(manager_userId, domain)
        isSiteManager = self.user_facade.check_if_email_is_site_manager(email_toSetAlumni, domain)
        if isSiteManager:
            self.user_facade.remove_site_manager(email_toSetAlumni, domain)
        self.labSystem.define_member_as_alumni_from_generator(email_toSetAlumni, domain)

    def add_alumni_from_lab_website(self, email_toSetAlumni, domain):
        """
        Define a lab member or lab manager as alumni in a specific website, from lab website.
        The given email_toSetAlumni must be associated with a Lab Member of the given website.
        """
        isSiteManager = self.user_facade.check_if_email_is_site_manager(email_toSetAlumni, domain)
        if isSiteManager:
            self.user_facade.remove_site_manager(email_toSetAlumni, domain)

    def remove_alumni_from_generator(self, manager_userId, email_toRemoveAlumni, domain):
        """
        Remove alumni in a specific website and set him again as member, from generator site.
        The given email_toRemoveAlumni must be associated with alumni of the given website.
        """
        self.user_facade.error_if_user_notExist(manager_userId)
        self.user_facade.error_if_user_not_logged_in(manager_userId)
        self.user_facade.error_if_user_is_not_site_manager(manager_userId, domain)
        self.labSystem.remove_alumni_from_generator(email_toRemoveAlumni, domain)

    def remove_site_manager_from_generator(self, nominator_manager_userId, manager_toRemove_email, domain):
        """
        Remove a manager from a specific website, from generator site.
        nomintator_manager_userId is the user that removes the manager.
        The given removed_manager_email must be associated with a manager of the given website.
        The permissions of the lab creator cannot be removed, it must always remain a Lab Manager
        """
        self.user_facade.error_if_user_notExist(nominator_manager_userId)
        self.user_facade.error_if_user_not_logged_in(nominator_manager_userId)
        self.user_facade.error_if_user_is_not_site_manager(nominator_manager_userId, domain)
        self.site_custom_facade.get_site_creator_email(domain)
        if manager_toRemove_email == self.site_custom_facade.get_site_creator_email(domain):
            raise Exception(ExceptionsEnum.PERMISSIONS_OF_SITE_CREATOR_CANNOT_BE_REMOVED.value)
        self.user_facade.remove_site_manager(manager_toRemove_email, domain)
        self.labSystem.remove_manager_permission_from_generator(manager_toRemove_email, domain)

    def register_new_LabMember_from_generator(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        """
        Define a new lab member in a specific website, from generator site.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        """
        self.user_facade.error_if_user_notExist(manager_userId)
        self.user_facade.error_if_user_not_logged_in(manager_userId)
        self.user_facade.error_if_user_is_not_site_manager(manager_userId, domain)
        self.labSystem.register_new_LabMember_from_generator(email_to_register, lab_member_fullName, lab_member_degree, domain)

    def login(self, google_token):
        """
        login into the generator system  (should be via Google in the future).
        A user can log in to the generator system using any email address of their choice.
        """
        return self.user_facade.get_or_create_user_by_token(google_token)

    def logout(self, userId):  # NOT USED ANYMORE
        """
        logout from the generator system (should be via Google in the future)
        """
        self.user_facade.error_if_user_notExist(userId)
        self.user_facade.logout(userId)

    def get_logged_in_user(self):
        """Get the currently logged-in user."""
        return self.user_facade.get_logged_in_user()

    def enter_generator_system(self):
        """Enter the generator system."""
        return self.user_facade.add_user()

    def get_all_custom_websites_of_manager(self, user_id):
        """Get all custom website details for specific manager (both generated and not generated sites).
        The details contain the domain, site name, and generated status."""
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        domains = self.user_facade.get_lab_websites(user_id)
        return self.site_custom_facade.get_custom_websites(domains)

    def get_custom_website(self, user_id, domain):
        """Get a custom website dto for specific manager and domain."""
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.user_facade.error_if_user_is_not_site_manager(user_id, domain)
        return self.site_custom_facade.get_site_by_domain(domain)

    def get_site_by_domain(self, domain):
        """Get a custom website dto for specific manager and domain."""
        return self.site_custom_facade.get_site_by_domain(domain)

    def reset_system(self):
        """
        Resets the entire system, clearing all users, websites, and lab-related data.
        """
        self.site_custom_facade.reset_system()
        self.labSystem.reset_system()

    def site_creator_resignation_from_generator(self, user_id, domain, nominated_email, new_role):
        """
        The site creator resigns from the site - from generator
        """
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        email = self.user_facade.get_email_from_token(user_id)
        self.site_custom_facade.error_if_user_is_not_site_creator(email, domain)
        self.site_custom_facade.set_site_creator(domain, nominated_email)
        if new_role != "manager":
            self.user_facade.remove_site_manager(email, domain)
        self.labSystem.site_creator_resignation_from_generator(domain, nominated_email, new_role)

    def site_creator_resignation_from_lab_website(self, domain, nominated_email, new_role):
        """
        The site creator resigns from the site - from lab website
        """
        self.site_custom_facade.set_site_creator(domain, nominated_email)
        if new_role != "manager":
            self.user_facade.remove_site_manager(nominated_email, domain)

    def delete_website(self, user_id, domain):
        """
        Delete a website if the user has permission.
        """
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.delete_website(domain)

    def get_gallery_images(self, domain):
        """
        Get the gallery images for a specific domain.
        """
        self.site_custom_facade.error_if_domain_not_exist(domain)
        return self.site_custom_facade.get_gallery_images(domain)

    def delete_gallery_image(self, user_id, domain, image_name):
        """
        Delete a specific image from the gallery.
        """
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.error_if_domain_not_exist(domain)
        self.site_custom_facade.delete_gallery_image(domain, image_name)