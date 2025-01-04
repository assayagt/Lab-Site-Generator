from src.main.DomainLayer.LabWebsites.LabSystem.LabSystemController import LabSystemController
from src.main.Util.Response import Response


class LabSystemService:
    _singleton_instance = None

    def __init__(self, lab_system_controller):
        if LabSystemService._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        # Get the instance of LabSystem
        self.lab_system_controller = lab_system_controller

    @staticmethod
    def get_instance(lab_system_controller):
        if LabSystemService._singleton_instance is None:
            LabSystemService._singleton_instance = LabSystemService(lab_system_controller)
        return LabSystemService._singleton_instance

    def enter_lab_website(self, domain):
        """Enter the lab system."""
        try:
            user_id = self.lab_system_controller.enter_lab_website(domain)
            return Response(user_id, "Entered lab website successfully")
        except Exception as e:
            return Response(None, str(e))

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        """Create a new lab website."""
        try:
            self.lab_system_controller.create_new_lab_website(domain, lab_members, lab_managers, site_creator)
            return Response(True, "Lab website created successfully")
        except Exception as e:
            return Response(None, str(e))

    def login(self, domain, user_id, email):
        """Log in a user to a specific lab website."""
        try:
            self.lab_system_controller.login(domain, user_id, email)
            return Response(True, "Login successful")
        except Exception as e:
            return Response(None, str(e))

    def logout(self, domain, user_id):
        """Log out a user from a specific lab website."""
        try:
            self.lab_system_controller.logout(domain, user_id)
            return Response(True, "Logout successful")
        except Exception as e:
            return Response(None, str(e))

    def crawl_for_publications(self):
        """Crawl for publications."""
        try:
            self.lab_system_controller.crawl_for_publications()
            return Response(True, "Crawling for publications completed successfully")
        except Exception as e:
            return Response(None, str(e))

    def initial_approve_publication_by_author(self, user_id, domain, publication_id):
        """Initial approve a publication by its author."""
        try:
            self.lab_system_controller.initial_approve_publication_by_author(user_id, domain, publication_id)
            return Response(True, "Publication approved successfully by author")
        except Exception as e:
            return Response(None, str(e))

    def final_approve_publication_by_manager(self, user_id, domain, publication_id):
        """Final approve a publication by a lab manager."""
        try:
            self.lab_system_controller.final_approve_publication_by_manager(user_id, domain, publication_id)
            return Response(True, "Publication approved successfully by manager")
        except Exception as e:
            return Response(None, str(e))

    def add_publication_manually(self, user_id, publication_dto, domain, authors_emails):
        """Add a publication manually to a lab website."""
        try:
            self.lab_system_controller.add_publication_manually(user_id, publication_dto, domain, authors_emails)
            return Response(True, "Publication added successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_approved_publications(self, domain):
        """Get all approved publications for a specific website."""
        try:
            publications = self.lab_system_controller.get_all_approved_publication(domain)
            return Response(publications, "Retrieved all approved publications successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_approved_publications_of_member(self, domain, email):
        """Get all approved publications of a specific member for a specific website."""
        try:
            publications = self.lab_system_controller.get_all_approved_publications_of_member(domain, email)
            return Response(publications, "Retrieved all approved publications for member successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_publication_video_link(self, user_id, domain, publication_id, video_link):
        """Set video link for a publication."""
        try:
            self.lab_system_controller.set_publication_video_link(user_id, domain, publication_id, video_link)
            return Response(True, "Video link added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_publication_git_link(self, user_id, domain, publication_id, git_link):
        """Set git link for a publication."""
        try:
            self.lab_system_controller.set_publication_git_link(user_id, domain, publication_id, git_link)
            return Response(True, "Git link added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_publication_presentation_link(self, user_id, domain, publication_id, presentation_link):
        """Set presentation link for a publication."""
        try:
            self.lab_system_controller.set_publication_presentation_link(user_id, domain, publication_id, presentation_link)
            return Response(True, "Presentation link added successfully")
        except Exception as e:
            return Response(None, str(e))

    def define_member_as_alumni(self, manager_user_id, member_email, domain):
        """Define a member as alumni."""
        try:
            self.lab_system_controller.define_member_as_alumni(manager_user_id, member_email, domain)
            return Response(True, "Member successfully defined as alumni")
        except Exception as e:
            return Response(None, str(e))

    def remove_manager_permission(self, manager_user_id, manager_to_remove_email, domain):
        """Remove administrative permissions from a lab manager."""
        try:
            self.lab_system_controller.remove_manager_permission(manager_user_id, manager_to_remove_email, domain)
            return Response(True, "Manager permissions removed successfully")
        except Exception as e:
            return Response(None, str(e))

    def approve_registration_request(self, domain, manager_userId, requested_email, requested_full_name):
        """Approve a registration request."""
        try:
            self.lab_system_controller.approve_registration_request(domain, manager_userId, requested_email, requested_full_name)
            return Response(True, "Registration request approved successfully")
        except Exception as e:
            return Response(None, str(e))

    def reject_registration_request(self, domain, manager_userId, requested_email):
        """Reject a registration request."""
        try:
            self.lab_system_controller.reject_registration_request(domain, manager_userId, requested_email)
            return Response(True, "Registration request rejected successfully")
        except Exception as e:
            return Response(None, str(e))