from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustomFacade import SiteCustomFacade, Template
from src.main.DomainLayer.LabGenerator.User.UserFacade import UserFacade
from src.main.DomainLayer.LabWebsites.LabSystem.LabSystem import LabSystem

class GeneratorSystemController:
    _singleton_instance = None

    def __init__(self):
        if GeneratorSystemController._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        self.user_facade = UserFacade()
        self.site_custom_facade = SiteCustomFacade()
        self.labSystem = LabSystem()

    @staticmethod
    def get_instance():
        if GeneratorSystemController._singleton_instance is None:
            GeneratorSystemController._singleton_instance = GeneratorSystemController()
        return GeneratorSystemController._singleton_instance
    
    def create_website(self, email, website_name, domain):
        """Create a website using SiteCustomFacade."""
         #TODO: check if user exists
        self.site_custom_facade.create_website(website_name, domain, None)
        #TODO: call the user facade

    def create_new_lab_website(self, domain, lab_members_emails, lab_managers_emails, site_creator_email):
        """
        Generates a new lab website once the custom site configuration is complete.
        """
        self.labSystem.create_new_lab_website(domain, lab_members_emails, lab_managers_emails, site_creator_email)

    def change_website_name(self, new_name, domain):
        """Change website details using SiteCustomFacade."""
        return self.site_custom_facade.change_site_name(domain, new_name)
    
    def change_website_domain(self,email, new_domain, domain):
        #TODO: check if user exists
        self.site_custom_facade.change_site_domain(domain, new_domain)
        self.user_facade.change_site_domain(domain, new_domain)
    
    def change_website_template(self,  domain, new_template = Template):
        return self.site_custom_facade.change_site_domain(domain, new_template)

    def add_components_to_site(self, domain, new_components=None):
         return self.site_custom_facade.add_components_to_site(domain, new_components)

    def create_new_site_manager(self, email, domain):
        """
        Define and add new manager to a specific website, from generator site.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        """
        self.user_facade.create_new_site_manager(email, domain)
        self.labSystem.create_new_site_manager_from_generator(domain, email)

    def register_new_LabMember_from_generator(self, email_to_register, domain):
        """
        Define a new lab member in a specific website, from generator site.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        """
        self.labSystem.register_new_LabMember_from_generator(email_to_register, domain)

    def login(self, userId, email):
        """
        login into the generator system  (should be via Google in the future).
        A user can log in to the generator system using any email address of their choice.
        """
        self.user_facade.error_if_user_notExist(userId)
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