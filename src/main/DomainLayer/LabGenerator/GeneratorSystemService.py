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

    def get_lab_system_controller(self):
        """Get the lab system controller through GeneratorSystemController."""
        return self.generator_system_controller.get_lab_system_controller()

    def enter_generator_system(self):
        """Enter the generator system through GeneratorSystemController."""
        try:
            user_id = self.generator_system_controller.enter_generator_system()
            return Response(user_id, "Entered generator system successfully")
        except Exception as e:
            return Response(None, str(e))

    def create_website(self, userId, website_name, domain, componentes, template):
        """Create a website through GeneratorSystemController."""
        try:
            self.generator_system_controller.create_website(userId, website_name, domain,componentes,template )
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

    def set_site_about_us_on_creation_from_generator(self, domain, about_us):
        """Set site about us on creation from generator through GeneratorSystemController."""
        try:
            self.generator_system_controller.set_site_about_us_on_creation_from_generator(domain, about_us)
            return Response(domain, "Site about us set successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_site_contact_info_on_creation_from_generator(self, domain, contact_info_dto):
        """Set site contact us on creation from generator through GeneratorSystemController."""
        try:
            self.generator_system_controller.set_site_contact_info_on_creation_from_generator(domain, contact_info_dto)
            return Response(domain, "Site contact us set successfully")
        except Exception as e:
            return Response(None, str(e))

    def change_site_logo_by_manager(self, user_id, domain):
        """Change the site logo by manager through GeneratorSystemController."""
        try:
            self.generator_system_controller.change_site_logo_by_manager(user_id, domain)
            return Response(domain, "Site logo changed successfully")
        except Exception as e:
            return Response(None, str(e))

    def change_site_home_picture_by_manager(self, user_id, domain):
        """Change the site home picture by manager through GeneratorSystemController."""
        try:
            self.generator_system_controller.change_site_home_picture_by_manager(user_id, domain)
            return Response(domain, "Site home picture changed successfully")
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

    def remove_site_manager_from_generator(self, nominator_manager_userId, manager_toRemove_email, domain):
        """
        Remove a manager from a specific website, from generator site.
        nomintator_manager_userId is the user that removes the manager.
        The given removed_manager_email must be associated with a manager of the given website.
        The permissions of the lab creator cannot be removed, it must always remain a Lab Manager
        """
        try:
            self.generator_system_controller.remove_site_manager_from_generator(nominator_manager_userId,
                                                                                manager_toRemove_email, domain)
            return Response(manager_toRemove_email, "Site manager removed successfully")
        except Exception as e:
            return Response(None, str(e))

    def register_new_LabMember_from_generator(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        """Register a new lab member through GeneratorSystemController."""
        try:
            self.generator_system_controller.register_new_LabMember_from_generator(manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain)
            return Response(email_to_register, "Lab member registered successfully")
        except Exception as e:
            return Response(None, str(e))

    def login(self,email, user_id):
        """Log in a user through GeneratorSystemController."""
        try:
            self.generator_system_controller.login(user_id, email)
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


    def get_all_custom_websites_of_manager(self, user_id):
        """Get all custom website details through GeneratorSystemController for specific manager (both generated and not generated sites).
        The details contain the domain, site name, and generated status"""
        try:
            websites = self.generator_system_controller.get_all_custom_websites_of_manager(user_id)
            return Response(websites, "Successfully retrieved custom websites")
        except Exception as e:
            return Response(None, str(e))

    def reset_system(self):
        """Reset the system through GeneratorSystemController."""
        try:
            self.generator_system_controller.reset_system()
            return Response(True, "System reset successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_custom_website(self, user_id, domain):
        """ Get a custom website dto for specific manager and domain, through GeneratorSystemController."""
        try:
            website = self.generator_system_controller.get_custom_website(user_id, domain)
            return Response({
                "domain": domain,
                "name": website.get_name(),
                "components": website.get_components(),
                "template": website.get_template(),
                "logo": website.logo,  # Include the logo
                "home_picture": website.home_picture  # Include the home picture
            }, "Successfully retrieved custom website")
        except Exception as e:
            return Response(None, str(e))
