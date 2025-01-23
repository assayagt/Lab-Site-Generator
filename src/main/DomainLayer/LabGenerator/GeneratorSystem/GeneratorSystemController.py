import os

from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustomFacade import SiteCustomFacade, Template
from src.main.DomainLayer.LabGenerator.User.UserFacade import UserFacade
from src.main.DomainLayer.LabWebsites.LabSystem.LabSystemController import LabSystemController

class GeneratorSystemController:
    _singleton_instance = None

    def __init__(self):
        if GeneratorSystemController._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        self.user_facade = UserFacade()
        self.site_custom_facade = SiteCustomFacade()
        self.labSystem = LabSystemController()

    @staticmethod
    def get_instance():
        if GeneratorSystemController._singleton_instance is None:
            GeneratorSystemController._singleton_instance = GeneratorSystemController()
        return GeneratorSystemController._singleton_instance

    def get_lab_system_controller(self):
        """Get the lab system controller."""
        return self.labSystem

    def create_website(self, user_id, website_name, domain, components, template):
        """Create a website using SiteCustomFacade."""
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        self.site_custom_facade.error_if_domain_already_exist(domain)
        email = self.user_facade.get_email_by_userId(user_id)
        self.site_custom_facade.create_new_site(domain, website_name, components, template, email)
        self.user_facade.create_new_site_manager(email, domain)

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
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
        self.labSystem.create_new_lab_website(domain, lab_members, lab_managers, site_creator)
        self.set_site_logo_on_site_creation(domain)
        self.set_site_home_picture_on_site_creation(domain)

    def set_site_about_us_on_creation_from_generator(self, domain, about_us):
        """
        Set the about us section on lab website creation. This function should be called after create_new_lab_website.
        """
        self.labSystem.set_site_about_us_from_generator(domain, about_us)

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
        self.labSystem.set_site_contact_info_from_generator(domain, contact_info_dto)

    def set_site_contact_info_by_manager_from_generator(self, user_id, domain, contact_info_dto):
        """
        Set the contact us section by manager
        """
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

        logo = logo_path if logo_path else None
        self.site_custom_facade.set_logo(domain, logo)

    def change_site_logo_by_manager(self, user_id, domain):
        """
        Change the site logo by the manager.
        """
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
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
        home_picture = home_picture_path if os.path.exists(home_picture_path) else None
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

    def login(self, userId, email):
        """
        login into the generator system  (should be via Google in the future).
        A user can log in to the generator system using any email address of their choice.
        """
        self.user_facade.error_if_user_notExist(userId)
        self.user_facade.error_if_email_is_not_valid(email)
        self.user_facade.login(userId, email)

    def logout(self, userId):
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
        self.user_facade.reset_system()
        self.site_custom_facade.reset_system()

    def site_creator_resignation(self, user_id, domain, nominated_email):
        """
        The site creator resigns from the site
        """
        self.user_facade.error_if_user_notExist(user_id)
        self.user_facade.error_if_user_not_logged_in(user_id)
        site_creator_email = self.site_custom_facade.get_site_creator_email(domain)
        self.site_custom_facade.error_if_user_is_not_site_creator(site_creator_email, domain)
        self.site_custom_facade.set_site_creator(domain, nominated_email)
        self.user_facade.remove_site_manager(site_creator_email, domain)
        self.user_facade.logout(user_id)
