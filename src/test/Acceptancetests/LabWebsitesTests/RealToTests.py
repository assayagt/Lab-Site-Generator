from src.test.Acceptancetests.LabWebsitesTests.BridgeToTests import BridgeToTests
from src.main.DomainLayer.LabWebsites.LabSystemService import LabSystemService


class RealToTests(BridgeToTests):
    def __init__(self, lab_system_controller):
        self.lab_system_service = LabSystemService.get_instance(lab_system_controller)

    def enter_lab_website(self, domain):
        return self.lab_system_service.enter_lab_website(domain)

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        return self.lab_system_service.create_new_lab_website(domain, lab_members, lab_managers, site_creator)

    def login(self, domain, user_id, email):
        return self.lab_system_service.login(domain, user_id, email)

    def logout(self, domain, user_id):
        return self.lab_system_service.logout(domain, user_id)

    def crawl_for_publications(self):
        return self.lab_system_service.crawl_for_publications()

    def initial_approve_publication_by_author(self, user_id, domain, publication_id):
        return self.lab_system_service.initial_approve_publication_by_author(user_id, domain, publication_id)

    def final_approve_publication_by_manager(self, user_id, domain, publication_id):
        return self.lab_system_service.final_approve_publication_by_manager(user_id, domain, publication_id)

    def add_publication_manually(self, user_id, domain, publication_link, git_link, video_link, presentation_link):
        return self.lab_system_service.add_publication_manually(user_id, domain, publication_link, git_link, video_link, presentation_link)

    def get_all_approved_publications(self, domain):
        return self.lab_system_service.get_all_approved_publication(domain)

    def get_all_approved_publications_of_member(self, domain, email):
        return self.lab_system_service.get_all_approved_publications_of_member(domain, email)

    def set_publication_video_link(self, user_id, domain, publication_id, video_link):
        return self.lab_system_service.set_publication_video_link(user_id, domain, publication_id, video_link)

    def set_publication_git_link(self, user_id, domain, publication_id, git_link):
        return self.lab_system_service.set_publication_git_link(user_id, domain, publication_id, git_link)

    def set_publication_presentation_link(self, user_id, domain, publication_id, presentation_link):
        return self.lab_system_service.set_publication_presentation_link(user_id, domain, publication_id, presentation_link)

    def define_member_as_alumni(self, manager_user_id, member_email, domain):
        return self.lab_system_service.define_member_as_alumni(manager_user_id, member_email, domain)

    def remove_manager_permission(self, manager_user_id, manager_to_remove_email, domain):
        return self.lab_system_service.remove_manager_permission(manager_user_id, manager_to_remove_email, domain)

    def approve_registration_request(self, domain, manager_userId, requested_email, requested_full_name, requested_degree):
        return self.lab_system_service.approve_registration_request(domain, manager_userId, requested_email, requested_full_name, requested_degree)

    def reject_registration_request(self, domain, manager_userId, requested_email):
        return self.lab_system_service.reject_registration_request(domain, manager_userId, requested_email)

    def create_new_site_manager_from_labWebsite(self, nominator_manager_userId, domain, nominated_manager_email):
        return self.lab_system_service.create_new_site_manager_from_labWebsite(nominator_manager_userId, domain, nominated_manager_email)

    def get_all_lab_managers(self, domain):
        return self.lab_system_service.get_all_lab_managers(domain)

    def get_all_lab_members(self, domain):
        return self.lab_system_service.get_all_lab_members(domain)

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        return self.lab_system_service.register_new_LabMember_from_labWebsite(manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain)

    def get_all_alumnis(self, domain):
        return self.lab_system_service.get_all_alumnis(domain)

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        return self.lab_system_service.set_secondEmail_by_member(userid, secondEmail, domain)

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        return self.lab_system_service.set_linkedin_link_by_member(userid, linkedin_link, domain)

    def set_fullName_by_member(self, userid, fullName, domain):
        return self.lab_system_service.set_fullName_by_member(userid, fullName, domain)

    def set_degree_by_member(self, userid, degree, domain):
        return self.lab_system_service.set_degree_by_member(userid, degree, domain)

    def set_bio_by_member(self, userid, bio, domain):
        return self.lab_system_service.set_bio_by_member(userid, bio, domain)

    def set_media_by_member(self, userid, media, domain):
        return self.lab_system_service.set_media_by_member(userid, media, domain)

    def get_all_lab_members_details(self, domain):
        return self.lab_system_service.get_all_lab_members_details(domain)

    def remove_alumni_from_labWebsite(self, manager_user_id, alumni_email, domain):
        return self.lab_system_service.remove_alumni_from_labWebsite(manager_user_id, alumni_email, domain)

    def reset_system(self):
        return self.lab_system_service.reset_system()

    def get_all_not_approved_publications_of_member(self, domain, user_id):
        return self.lab_system_service.get_all_not_approved_publications_of_member(domain, user_id)
    
    def remove_publication(self, user_id, domain, publication_id):
        return self.lab_system_service.remove_publication(user_id, domain, publication_id)