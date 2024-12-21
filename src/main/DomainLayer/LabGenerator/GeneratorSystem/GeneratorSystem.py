from main.DomainLayer.LabGenerator.SiteCustom import SiteCustomFacade, Template
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
        site =  self.site_custom_facade.create_website(website_name, domain, components)
        self.user_facade.addCustomWebsite(site) ##TODO: add function to facade

    def change_website_name(self, new_name, domain):
        """Change website details using SiteCustomFacade."""
        return self.site_custom_facade.change_site_name(domain, new_name)
    
    def change_website_domain(self,  new_domain, domain):
        return self.site_custom_facade.change_site_domain(domain, new_domain)
    
    def change_website_template(self,  domain, new_template = Template):
        return self.site_custom_facade.change_site_domain(domain, new_template)

    def add_components_to_site(self, domain, new_components=None):
         return self.site_custom_facade.add_components_to_site(domain, new_components)

    def login(self, email, password): #TODO: change a little
        """Log in a user using UserFacade."""
        return self.user_facade.login(email, password)

    def logout(self):
        """Log out the current user using UserFacade."""
        return self.user_facade.logout()

    def get_logged_in_user(self):
        """Get the currently logged-in user."""
        return self.user_facade.get_logged_in_user()