from src.main.DomainLayer.LabGenerator.GeneratorSystem import GeneratorSystemController
from src.main.Util.Response import Response
import src.main.DomainLayer.LabGenerator.SiteCustom.Template as Template


class GeneratorSystemService:
    _singleton_instance = None

    def __init__(self):
        if GeneratorSystemService._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        # Get the instance of GeneratorSystemController
        self.generator_system_controller = GeneratorSystemController.GeneratorSystemController.get_instance()

    @staticmethod
    def get_instance():
        if GeneratorSystemService._singleton_instance is None:
            GeneratorSystemService._singleton_instance = GeneratorSystemService()
        return GeneratorSystemService._singleton_instance

    def enter_generator_system(self):
        """Enter the generator system through GeneratorSystemController."""
        try:
            user_id = self.generator_system_controller.enter_generator_system()
            return Response(user_id, "Entered generator system successfully")
        except Exception as e:
            return Response(None, str(e))

    def create_website(self, email, website_name, domain, componentes=None, template=None):
        """Create a website through GeneratorSystemController."""
        try:
            self.generator_system_controller.create_website(email, website_name, domain, componentes, template)
            return Response(domain, "Website created successfully")
        except Exception as e:
            return Response(None, str(e))

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        """Create a new lab website through GeneratorSystemController."""
        try:
            self.generator_system_controller.create_new_lab_website(domain, lab_members, lab_managers, site_creator)
            return Response(domain, "Lab website created successfully")
        except Exception as e:
            return Response(None, str(e))

    def change_website_name(self, user_id, new_name, domain):
        """Change website name through GeneratorSystemController."""
        try:
            self.generator_system_controller.change_website_name(user_id, new_name, domain)
            return Response(new_name, "Website name changed successfully")
        except Exception as e:
            return Response(None, str(e))


    def change_website_domain(self, user_id, new_domain, domain):
        """Change website domain through GeneratorSystemController."""
        try:
            self.generator_system_controller.change_website_domain(user_id, new_domain, domain)
            return Response(new_domain, "Website domain changed successfully")
        except Exception as e:
            return Response(None, str(e))

    def change_website_template(self, user_id, domain, new_template=Template):
        """Change website template through GeneratorSystemController."""
        try:
            self.generator_system_controller.change_website_template(user_id, domain, new_template)
            return Response(True, "Website template changed successfully")
        except Exception as e:
            return Response(None, str(e))

    def add_components_to_site(self, user_id, domain, new_components=None):
        """Add components to the site through GeneratorSystemController."""
        try:
            self.generator_system_controller.add_components_to_site(user_id, domain, new_components)
            return Response(new_components, "Website components added successfully")
        except Exception as e:
            return Response(None, str(e))

    def create_new_site_manager(self, nominator_manager_userId, nominated_manager_email, domain):
        """Create a new site manager through GeneratorSystemController."""
        try:
            self.generator_system_controller.create_new_site_manager(nominator_manager_userId, nominated_manager_email, domain)
            return Response(nominated_manager_email, "Site manager created successfully")
        except Exception as e:
            return Response(None, str(e))

    def register_new_LabMember_from_generator(self, manager_userId, email_to_register, lab_member_fullName, domain):
        """Register a new lab member through GeneratorSystemController."""
        try:
            self.generator_system_controller.register_new_LabMember_from_generator(manager_userId, email_to_register, lab_member_fullName, domain)
            return Response(email_to_register, "Lab member registered successfully")
        except Exception as e:
            return Response(None, str(e))

    def login(self,email, user_id):
        """Log in a user through GeneratorSystemController."""
        try:
            self.generator_system_controller.login(email, user_id)
            return Response(user_id, "User logged in successfully")
        except Exception as e:
            return Response(None, str(e))

    def logout(self, user_id):
        """Log out the current user through GeneratorSystemController."""
        try:
            self.generator_system_controller.logout(user_id)
            return Response(True, "User logged out successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_logged_in_user(self):
        """Get the currently logged-in user through GeneratorSystemController."""
        try:
            user = self.generator_system_controller.get_logged_in_user()
            return Response(user, "Successfully retrieved logged-in user")
        except Exception as e:
            return Response(None, str(e))


    def get_custom_websites(self, user_id):
        """Get all lab websites through GeneratorSystemController."""
        try:
            websites = self.generator_system_controller.get_custom_websites(user_id)
            return Response(websites, "Successfully retrieved lab websites")
        except Exception as e:
            return Response(None, str(e))

    def get_lab_websites(self, user_id):
        """Get a lab website through GeneratorSystemController."""
        try:
            websites = self.generator_system_controller.get_lab_websites(user_id)
            return Response(websites, "Successfully retrieved lab website")
        except Exception as e:
            return Response(None, str(e))

    def reset_system(self):
        """Reset the system through GeneratorSystemController."""
        try:
            self.generator_system_controller.reset_system()
            return Response(True, "System reset successfully")

    def get_custom_website(self, user_id, domain):
        """Get a custom website through GeneratorSystemController."""
        try:
            website = self.generator_system_controller.get_custom_website(user_id, domain)
            return Response({
                    "domain": domain,
                    "name": website.get_name(),
                    "components": website.get_components(),
                    "template": website.get_template()
                }, "Successfully retrieved custom website")
        except Exception as e:
            return Response(None, str(e))