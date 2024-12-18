from main.DomainLayer.LabGenerator.SiteCustom import SiteCustomFacade
from main.DomainLayer.LabGenerator.User import UserFacade


class GeneratorSystem:
    _singleton_instance = None

    def __init__(self):
        if GeneratorSystem._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        self.user_facade = UserFacade()
        self.site_custom_facade = SiteCustomFacade()

    @staticmethod
    def get_instance():
        if GeneratorSystem._singleton_instance is None:
            GeneratorSystem._singleton_instance = GeneratorSystem()
        return GeneratorSystem._singleton_instance
    
    def create_website(self, website_name, domain, components):
        """Create a website using SiteCustomFacade."""
        return self.site_custom_facade.create_website(website_name, domain, components)

    def change_website(self, website_name, new_name=None, new_domain=None, new_components=None):
        """Change website details using SiteCustomFacade."""
        return self.site_custom_facade.change_website(website_name, new_name, new_domain, new_components)

    def login(self, email, password):
        """Log in a user using UserFacade."""
        return self.user_facade.login(email, password)

    def logout(self):
        """Log out the current user using UserFacade."""
        return self.user_facade.logout()

    def get_logged_in_user(self):
        """Get the currently logged-in user."""
        return self.user_facade.get_logged_in_user()