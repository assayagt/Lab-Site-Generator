from abc import ABC, abstractmethod

class BridgeToTests(ABC):
    @abstractmethod
    def enter_generator_system(self):
        """Enter the generator system."""
        pass

    def get_lab_system_controller(self):
        """Get the lab system controller through GeneratorSystemController."""
        pass

    @abstractmethod
    def create_website(self, email, website_name, domain, components, template):
        """Create a website."""
        pass

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator, google_scholar_link):
        """Create a new lab website."""
        pass

    @abstractmethod
    def change_website_name(self, userId, new_name, domain):
        """Change the website's name."""
        pass

    @abstractmethod
    def change_website_domain(self, userId, new_domain, domain):
        """Change the website's domain."""
        pass

    @abstractmethod
    def change_website_template(self, userId, domain, new_template=None):
        """Change the website's template."""
        pass

    @abstractmethod
    def add_components_to_site(self, userId, domain, new_components):
        """Add components to the site."""
        pass

    def create_new_site_manager(self, nominator_manager_userId, nominated_manager_email, domain):
        """Create a new site manager."""
        pass

    def register_new_LabMember_from_generator(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        """Register a new lab member."""
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

    @abstractmethod
    def get_site_by_domain(self, domain):
        """Get a site by its domain."""
        pass

    def reset_system(self):
        """Reset the system."""
        pass

    @abstractmethod
    def change_site_logo_by_manager(self, user_id, domain):
        """Change the site's logo."""
        pass

    @abstractmethod
    def remove_site_manager_from_generator(self, nominator_manager_userId, manager_toRemove_email, domain):
        """Remove a site manager."""
        pass

    @abstractmethod
    def add_alumni_from_generator(self, manager_userId, email_toSetAlumni, domain):
        """Add an alumni."""
        pass

    @abstractmethod
    def remove_alumni_from_generator(self, manager_userId, email_toRemoveAlumni, domain):
        """Remove an alumni."""
        pass
    
    @abstractmethod
    def delete_website(self, user_id, domain):
        """Delete a website."""
        pass

    def site_creator_resignation_from_generator(self, site_creator_user_id, domain, nominated_email, new_role):
        """Handle site creator resignation."""
        pass
