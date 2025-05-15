import threading

from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabWebsites.LabSystem.LabSystemController import LabSystemController
from src.main.Util.Response import Response


class LabSystemService:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, lab_system_controller):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(LabSystemService, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, lab_system_controller):
        if self._initialized:
            return

        self.lab_system_controller = lab_system_controller
        self._initialized = True

    @classmethod
    def get_instance(cls, lab_system_controller):
        return cls(lab_system_controller)

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance. Useful for unit tests."""
        with cls._instance_lock:
            cls._instance = None

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
            #check if the exception is USER_NOT_REGISTERED
            if e == ExceptionsEnum.USER_NOT_REGISTERED.value:
                return Response(False, str(e))
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

    def initial_approve_publication_by_author(self, user_id, domain, notification_id):
        """Initial approve a publication by its author."""
        try:
            self.lab_system_controller.initial_approve_publication_by_author(user_id, domain, notification_id)
            return Response(True, "Publication approved successfully by author")
        except Exception as e:
            return Response(None, str(e))

    def final_approve_publication_by_manager(self, user_id, domain, notification_id):
        """Final approve a publication by a lab manager."""
        try:
            self.lab_system_controller.final_approve_publication_by_manager(user_id, domain, notification_id)
            return Response(True, "Publication approved successfully by manager")
        except Exception as e:
            return Response(None, str(e))

    def reject_publication(self, user_id, domain, notification_id):
        """Reject a publication."""
        try:
            self.lab_system_controller.reject_publication(user_id, domain, notification_id)
            return Response(True, "Publication rejected successfully")
        except Exception as e:
            return Response(None, str(e))

    def add_publication_manually(self, user_id, domain, publication_link, git_link, video_link, presentation_link):
        """Add a publication manually to a lab website."""
        try:
            self.lab_system_controller.add_publication_manually(user_id, domain, publication_link, git_link, video_link, presentation_link)
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

    def get_all_approved_publications_of_member(self, domain, user_id):
        """Get all approved publications of a specific member for a specific website."""
        try:
            publications = self.lab_system_controller.get_all_approved_publications_of_member(domain, user_id)
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
            self.lab_system_controller.set_publication_git_link_by_author(user_id, domain, publication_id, git_link)
            return Response(True, "Git link added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_publication_presentation_link(self, user_id, domain, publication_id, presentation_link):
        """Set presentation link for a publication."""
        try:
            self.lab_system_controller.set_publication_presentation_link_by_author(user_id, domain, publication_id, presentation_link)
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

    def approve_registration_request(self, domain, manager_userId, requested_full_name, requested_degree, notification_id):
        """Approve a registration request."""
        try:
            self.lab_system_controller.approve_registration_request(domain, manager_userId, requested_full_name, requested_degree, notification_id)
            return Response(True, "Registration request approved successfully")
        except Exception as e:
            return Response(None, str(e))

    def reject_registration_request(self, domain, manager_userId, notification_id):
        """Reject a registration request."""
        try:
            self.lab_system_controller.reject_registration_request(domain, manager_userId, notification_id)
            return Response(True, "Registration request rejected successfully")
        except Exception as e:
            return Response(None, str(e))

    def create_new_site_manager_from_labWebsite(self, nominator_manager_userId, domain, nominated_manager_email):
        """Create a new site manager."""
        try:
            self.lab_system_controller.create_new_site_manager_from_labWebsite(nominator_manager_userId, domain, nominated_manager_email)
            return Response(True, "Site manager created successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_lab_managers(self, domain):
        """Get all lab managers, including the site creator."""
        try:
            lab_managers = self.lab_system_controller.get_all_lab_managers(domain)
            return Response(lab_managers, "Retrieved all lab managers successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_lab_members(self, domain):
        """Get all lab members."""
        try:
            lab_members = self.lab_system_controller.get_all_lab_members(domain)
            return Response(lab_members, "Retrieved all lab members successfully")
        except Exception as e:
            return Response(None, str(e))

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        """Register a new lab member."""
        try:
            self.lab_system_controller.register_new_LabMember_from_labWebsite(manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain)
            return Response(True, "Lab member registered successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_alumnis(self, domain):
        """Get all alumnis."""
        try:
            alumnis = self.lab_system_controller.get_all_alumnis(domain)
            return Response(alumnis, "Retrieved all alumnis successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        try:
            self.lab_system_controller.set_secondEmail_by_member(userid, secondEmail, domain)
            return Response(True, "Second email added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        try:
            self.lab_system_controller.set_linkedin_link_by_member(userid, linkedin_link, domain)
            return Response(True, "LinkedIn link added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_fullName_by_member(self, userid, fullName, domain):
        try:
            self.lab_system_controller.set_fullName_by_member(userid, fullName, domain)
            return Response(True, "Full name added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_degree_by_member(self, userid, degree, domain):
        try:
            self.lab_system_controller.set_degree_by_member(userid, degree, domain)
            return Response(True, "Degree added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_bio_by_member(self, userid, bio, domain):
        try:
            self.lab_system_controller.set_bio_by_member(userid, bio, domain)
            return Response(True, "Bio added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_media_by_member(self, userid, media, domain):
        try:
            self.lab_system_controller.set_media_by_member(userid, media, domain)
            return Response(True, "Media added successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_pending_registration_emails(self, userid, domain):
        try:
            pending_registration_emails = self.lab_system_controller.get_pending_registration_emails(userid, domain)
            return Response(pending_registration_emails, "Retrieved all pending registration emails successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_members_names(self, domain):
        '''
        returns all lab members + managers + site creator + alumnis names
        '''
        try:
            members_names = self.lab_system_controller.get_all_members_names(domain)
            return Response(members_names, "Retrieved all members names successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_about_us(self, domain):
        try:

            about_us = self.lab_system_controller.get_about_us(domain)
            return Response(about_us, "Retrieved about us successfully")
        except Exception as e:
            return Response(None, str(e))
        
    def get_contact_us(self, domain):
        try:
            about_us = self.lab_system_controller.get_contact_us(domain)
            return Response(about_us, "Retrieved about us successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_lab_members_details(self, domain):
        """Get all lab members."""
        try:
            lab_members = self.lab_system_controller.get_all_lab_members_details(domain)
            return Response(lab_members, "Retrieved all lab members successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_lab_managers_details(self, domain):
        """Get all lab members."""
        try:
            lab_managers = self.lab_system_controller.get_all_lab_managers_details(domain)
            return Response(lab_managers, "Retrieved all lab managers successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_alumnis_details(self, domain):
        """Get all lab members."""
        try:
            lab_alumnis = self.lab_system_controller.get_all_alumnis_details(domain)
            return Response(lab_alumnis, "Retrieved all lab alumnis successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_user_details(self, user_id, domain):
        """Get user details."""
        try:
            user_details = self.lab_system_controller.get_user_details(user_id, domain)
            return Response(user_details, "Retrieved user details successfully")
        except Exception as e:
            return Response(None, str(e))
        

    def set_site_about_us_from_labWebsite(self, userId, domain, about_us):
        """
        Set the about us section of the website.
        """
        try:
            self.lab_system_controller.set_site_about_us_from_labWebsite(userId, domain, about_us)
            return Response(True, "About us added successfully")
        except Exception as e:
            return Response(None, str(e))

    def set_site_contact_info_from_labWebsite(self, userId, domain, contact_info_dto):
        """
        Set the contact info section of the website.
        """
        try:
            self.lab_system_controller.set_site_contact_info_from_labWebsite(userId, domain, contact_info_dto)
            return Response(True, "Contact info added successfully")
        except Exception as e:
            return Response(None, str(e))

    def site_creator_resignation_from_lab_website(self, user_id, domain, nominate_email, new_role):
        """
        Site creator resignation from lab website.
        """
        try:
            self.lab_system_controller.site_creator_resignation_from_lab_website(user_id, domain, nominate_email, new_role)
            return Response(True, "Site creator resigned successfully")
        except Exception as e:
            return Response(None, str(e))

    def site_creator_resignation_from_generator(self, domain, nominate_email, new_role):
        """
        Site creator resignation from generator.
        """
        try:
            self.lab_system_controller.site_creator_resignation_from_generator(domain, nominate_email, new_role)
            return Response(True, "Site creator resigned successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_member_notifications(self, user_id, domain):
        try:
            notifications = self.lab_system_controller.get_all_member_notifications(user_id, domain)
            return Response(notifications, "Retrieved all notifications successfully")
        except Exception as e:
            return Response(None, str(e))

    def get_all_publications(self, user_id, domain):
        try:
            publications = self.lab_system_controller.get_all_publications(user_id, domain)
            return Response(publications, "Retrieved all publications successfully")
        except Exception as e:
            return Response(None, str(e))

    def connect_user_socket(self, email, domain, sid):
        try:
            self.lab_system_controller.connect_user_socket(email, domain, sid)
            return Response(True, "User socket connected successfully")
        except Exception as e:
            return Response(None, str(e))

    def disconnect_user_socket(self, sid):
        try:
            self.lab_system_controller.disconnect_user_socket(sid)
            return Response(True, "User socket disconnected successfully")
        except Exception as e:
            return Response(None, str(e))

    def reset_system(self):
        try:
            self.lab_system_controller.reset_system()
            return Response(True, "System reset successfully")
        except Exception as e:
            return Response(None, str(e))