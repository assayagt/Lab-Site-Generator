import base64
import os
import threading

from src.main.DomainLayer.LabGenerator.GeneratorSystem.GeneratorSystemController import GeneratorSystemController
from src.main.Util.Response import Response
import src.main.DomainLayer.LabGenerator.SiteCustom.Template as Template


class GeneratorSystemService:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(GeneratorSystemService, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Initialize only once
        self.generator_system_controller = GeneratorSystemController()
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

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator, creator_scholar_link):
        """Create a new lab website through GeneratorSystemController."""
        try:
            self.generator_system_controller.create_new_lab_website(domain, lab_members, lab_managers, site_creator, creator_scholar_link)
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

    def set_site_about_us_by_manager_from_generator(self, user_id, domain, about_us):
        """Set site about us by manager from generator through GeneratorSystemController."""
        try:
            self.generator_system_controller.set_site_about_us_by_manager_from_generator(user_id, domain, about_us)
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

    def set_site_contact_info_by_manager_from_generator(self, user_id, domain, contact_info_dto):
        """Set site contact us by manager from generator through GeneratorSystemController."""
        try:
            self.generator_system_controller.set_site_contact_info_by_manager_from_generator(user_id, domain, contact_info_dto)
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

    def create_new_site_manager_from_lab_website(self, nominated_manager_email, domain):
        """Create a new site manager from lab website"""
        try:
            self.generator_system_controller.create_new_site_manager_from_lab_website(nominated_manager_email, domain)
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

    def login(self, user_id, email):
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
            about_us = self.generator_system_controller.get_site_about_us_from_generator(domain)
            contact_us = self.generator_system_controller.get_contact_info_from_generator(domain)
            logo_path = website.logo  # Ensure `website.logo` contains the full file path
            gallery_images = self.generator_system_controller.get_gallery_images(domain)
            if logo_path and os.path.exists(logo_path):
                # Check the file extension
                extension = os.path.splitext(logo_path)[1].lower()
                if extension in ['.svg', '.png', '.jpg', '.jpeg']:
                    with open(logo_path, "rb") as logo_file:
                        logo_base64 = base64.b64encode(logo_file.read()).decode()
                        logo_data_url = f"data:image/{extension[1:]};base64,{logo_base64}"  # Adjust MIME type dynamically
                else:
                    logo_data_url = None
            else:
                logo_data_url = None
            return Response({
                "domain": domain,
                "name": website.get_name(),
                "components": website.get_components(),
                "template": None if website.get_template() is None else website.get_template().value, 
                "logo": logo_data_url,  # Include the logo
                "home_picture": website.home_picture,  # Include the home picture
                "about_us": about_us,
                "contact_us": contact_us,
                "gallery_images": gallery_images
            }, "Successfully retrieved custom website")
        except Exception as e:
            return Response(None, str(e))

    def get_site_by_domain(self, domain):
        try:
            website = self.generator_system_controller.get_site_by_domain(domain)
            logo_path = website.get_logo()  # Ensure `website.logo` contains the full file path
            gallery_images = self.generator_system_controller.get_gallery_images(domain)
            if logo_path and os.path.exists(logo_path):
                # Check the file extension
                extension = os.path.splitext(logo_path)[1].lower()
                if extension in ['.svg', '.png', '.jpg', '.jpeg']:
                    with open(logo_path, "rb") as logo_file:
                        if extension == '.svg':
                            mime_type = 'image/svg+xml'
                        elif extension == '.png':
                            mime_type = 'image/png'
                        elif extension == '.jpg' or extension == '.jpeg':
                            mime_type = 'image/jpeg'
                        else:
                            mime_type = 'application/octet-stream'  # Default for unsupported types
        
                        logo_base64 = base64.b64encode(logo_file.read()).decode()
                        logo_data_url = f"data:{mime_type};base64,{logo_base64}"  # Set dynamic MIME type
                else:
                    logo_data_url = None
            else:
                logo_data_url = None
            homePhoto_path = website.get_home_picture()  # Ensure `website.logo` contains the full file path
            print(homePhoto_path)
            if homePhoto_path and os.path.exists(homePhoto_path):
                # Check the file extension
                extension = os.path.splitext(homePhoto_path)[1].lower()
                if extension in ['.svg', '.png', '.jpg', '.jpeg']:
                    with open(homePhoto_path, "rb") as picture_file:
                        if extension == '.svg':
                            mime_type = 'image/svg+xml'
                        elif extension == '.png':
                            mime_type = 'image/png'
                        elif extension == '.jpg' or extension == '.jpeg':
                            mime_type = 'image/jpeg'
                        else:
                            mime_type = 'application/octet-stream'  # Default for unsupported types
        
                        picture_base64 = base64.b64encode(picture_file.read()).decode()
                        picture_data_url = f"data:{mime_type};base64,{picture_base64}"  # Set dynamic MIME type
                else:
                    picture_data_url = None
            else:
                picture_data_url = None
            return Response({
                "domain": domain,
                "name": website.get_name(),
                "components": website.get_components(),
                "template": website.get_template().value,
                "logo": logo_data_url,  # Include the logo
                "home_picture":  picture_data_url,  # Include the home picture,
                "gallery_images": gallery_images
            }, "Successfully retrieved custom website")
        except Exception as e:
            return Response(None, str(e))


    def site_creator_resignation_from_generator(self, site_creator_user_id, domain, nominated_email, new_role):
        """Resignation of the site creator through GeneratorSystemController."""
        try:
            self.generator_system_controller.site_creator_resignation_from_generator(site_creator_user_id, domain, nominated_email, new_role)
            return Response(domain, "Site creator resigned successfully")
        except Exception as e:
            return Response(None, str(e))

    def site_creator_resignation_from_lab_website(self, domain, nominated_email, new_role):
        """Resignation of the site creator from lab website."""
        try:
            self.generator_system_controller.site_creator_resignation_from_lab_website(domain, nominated_email, new_role)
            return Response(domain, "Site creator resigned successfully")
        except Exception as e:
            return Response(None, str(e))

    def add_alumni_from_generator(self, manager_userId, email_toSetAlumni, domain):
        """Set a lab member as alumni through GeneratorSystemController."""
        try:
            self.generator_system_controller.add_alumni_from_generator(manager_userId, email_toSetAlumni, domain)
            return Response(email_toSetAlumni, "Lab member set as alumni successfully")
        except Exception as e:
            return Response(None, str(e))

    def add_alumni_from_lab_website(self, email_toSetAlumni, domain):
        """Set a lab member as alumni from lab website."""
        try:
            self.generator_system_controller.add_alumni_from_lab_website(email_toSetAlumni, domain)
            return Response(email_toSetAlumni, "Lab member set as alumni successfully")
        except Exception as e:
            return Response(None, str(e))

    def remove_alumni_from_generator(self, manager_userId, email_toRemoveAlumni, domain):
        """Remove a lab member from alumni through GeneratorSystemController."""
        try:
            self.generator_system_controller.remove_alumni_from_generator(manager_userId, email_toRemoveAlumni, domain)
            return Response(email_toRemoveAlumni, "Lab member removed from alumni successfully")
        except Exception as e:
            return Response(None, str(e))

    def delete_website(self, user_id, domain):
        """
        Delete a website if the user has permission.
        
        Args:
            user_id (str): The ID of the user requesting the deletion
            domain (str): The domain of the website to delete
            
        Returns:
            Response: A response object indicating success or failure
        """
        try:
            # Delete the website
            self.generator_system_controller.delete_website(user_id, domain)
            return Response(True, "Website deleted successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_gallery_images(self, domain):
        """
        Get the gallery images of a website.

        Args:
            domain (str): The domain of the website

        Returns:
            Response: A response object containing the gallery images or an error message
        """
        try:
            images = self.generator_system_controller.get_gallery_images(domain)
            return Response(images, "Gallery images retrieved successfully")
        except Exception as e:
            return Response(None, str(e))

    def delete_gallery_image(self, user_id, domain, image_name):
        """
        Delete a specific gallery image from the website.

        Args:
            domain (str): The domain of the website
            image_name (str): The name of the image to delete

        Returns:
            Response: A response object indicating success or failure
        """
        try:
            self.generator_system_controller.delete_gallery_image(user_id, domain, image_name)
            return Response(True, "Gallery image deleted successfully")
        except Exception as e:
            return Response(None, str(e))