from abc import ABC, abstractmethod

class BridgeToTests(ABC):
    @abstractmethod
    def enter_generator_system(self):
        """Enter the generator system."""
        pass

    @abstractmethod
    def create_website(self, email, website_name, domain):
        """Create a website."""
        pass

    @abstractmethod
    def change_website_name(self, new_name, domain):
        """Change the website's name."""
        pass

    @abstractmethod
    def change_website_domain(self, email, new_domain, domain):
        """Change the website's domain."""
        pass

    @abstractmethod
    def change_website_template(self, domain, new_template=None):
        """Change the website's template."""
        pass

    @abstractmethod
    def add_components_to_site(self, domain, new_components=None):
        """Add components to the site."""
        pass

    @abstractmethod
    def login(self, user_id, email):
        """Log in a user."""
        pass

    @abstractmethod
    def logout(self, user_id):
        """Log out the current user."""
        pass

    @abstractmethod
    def get_logged_in_user(self):
        """Get the currently logged-in user."""
        pass
