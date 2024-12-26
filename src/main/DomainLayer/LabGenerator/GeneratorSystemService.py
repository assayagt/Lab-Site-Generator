from main.DomainLayer.LabGenerator.GeneratorSystem import GeneratorSystemController


class GeneratorSystemService:
    _singleton_instance = None

    def __init__(self):
        if GeneratorSystemService._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        # Get the instance of GeneratorSystemController
        self.generator_system_controller = GeneratorSystemController.get_instance()

    @staticmethod
    def get_instance():
        if GeneratorSystemService._singleton_instance is None:
            GeneratorSystemService._singleton_instance = GeneratorSystemService()
        return GeneratorSystemService._singleton_instance

    def enter_generator_system(self):
        """Enter the generator system through GeneratorSystemController."""
        return self.generator_system_controller.enter_generator_system()

    def create_website(self, email, website_name, domain):
        """Create a website through GeneratorSystemController."""
        return self.generator_system_controller.create_website(email, website_name, domain)

    def change_website_name(self, new_name, domain):
        """Change website name through GeneratorSystemController."""
        return self.generator_system_controller.change_website_name(new_name, domain)

    def change_website_domain(self, email, new_domain, domain):
        """Change website domain through GeneratorSystemController."""
        return self.generator_system_controller.change_website_domain(email, new_domain, domain)

    def change_website_template(self, domain, new_template=Template):
        """Change website template through GeneratorSystemController."""
        return self.generator_system_controller.change_website_template(domain, new_template)

    def add_components_to_site(self, domain, new_components=None):
        """Add components to the site through GeneratorSystemController."""
        return self.generator_system_controller.add_components_to_site(domain, new_components)

    def login(self, email):
        """Log in a user through GeneratorSystemController."""
        return self.generator_system_controller.login(email)

    def logout(self):
        """Log out the current user through GeneratorSystemController."""
        return self.generator_system_controller.logout()

    def get_logged_in_user(self):
        """Get the currently logged-in user through GeneratorSystemController."""
        return self.generator_system_controller.get_logged_in_user()
