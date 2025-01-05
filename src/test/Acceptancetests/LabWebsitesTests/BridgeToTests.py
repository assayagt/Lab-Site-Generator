from abc import ABC, abstractmethod


class BridgeToTests(ABC):

    def enter_lab_website(self, domain):
        """Enter a lab website."""
        pass

    @abstractmethod
    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        """Create a new lab website."""
        pass

    @abstractmethod
    def login(self, domain, user_id, email):
        """Log in a user to a specific lab website."""
        pass

    @abstractmethod
    def logout(self, domain, user_id):
        """Log out a user from a specific lab website."""
        pass

    @abstractmethod
    def crawl_for_publications(self):
        """Crawl for publications."""
        pass

    @abstractmethod
    def initial_approve_publication_by_author(self, user_id, domain, publication_id):
        """Initial approve a publication by its author."""
        pass

    @abstractmethod
    def final_approve_publication_by_manager(self, user_id, domain, publication_id):
        """Final approve a publication by a lab manager."""
        pass

    @abstractmethod
    def add_publication_manually(self, user_id, publication_dto, domain, authors_emails):
        """Add a publication manually to a lab website."""
        pass

    @abstractmethod
    def get_all_approved_publications(self, domain):
        """Get all approved publications for a specific website."""
        pass

    @abstractmethod
    def get_all_approved_publications_of_member(self, domain, email):
        """Get all approved publications of a specific member for a specific website."""
        pass

    @abstractmethod
    def set_publication_video_link(self, user_id, domain, publication_id, video_link):
        """Set video link for a publication."""
        pass

    @abstractmethod
    def set_publication_git_link(self, user_id, domain, publication_id, git_link):
        """Set git link for a publication."""
        pass

    @abstractmethod
    def set_publication_presentation_link(self, user_id, domain, publication_id, presentation_link):
        """Set presentation link for a publication."""
        pass

    @abstractmethod
    def define_member_as_alumni(self, manager_user_id, member_email, domain):
        """Define a member as alumni."""
        pass

    @abstractmethod
    def remove_manager_permission(self, manager_user_id, manager_to_remove_email, domain):
        """Remove administrative permissions from a lab manager."""
        pass

    @abstractmethod
    def approve_registration_request(self, domain, manager_userId, requested_email, requested_full_name):
        """Approve a registration request."""
        pass

    def reject_registration_request(self, domain, manager_userId, requested_email):
        """Reject a registration request."""
        pass

    def create_new_site_manager_from_labWebsite(self, nominator_manager_userId, domain, nominated_manager_email):
        """Create a new site manager from a lab website."""
        pass

    def get_all_lab_managers(self, domain):
        """Get all lab managers."""
        pass

    def get_all_lab_members(self, domain):
        """Get all lab members."""
        pass

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, lab_member_fullName, domain):
        """Register a new lab member from a lab website."""
        pass

    def get_all_alumnis(self, domain):
        """Get all alumni."""
        pass

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        """Set second email for a member."""
        pass

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        """Set linkedin link for a member."""
        pass

    def set_fullName_by_member(self, userid, fullName, domain):
        """Set full name for a member."""
        pass

    def set_degree_by_member(self, userid, degree, domain):
        """Set degree for a member."""
        pass

    def set_bio_by_member(self, userid, bio, domain):
        """Set bio for a member."""
        pass