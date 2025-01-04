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

    def add_publication_manually(self, user_id, publication_dto, domain, authors_emails):
        return self.lab_system_service.add_publication_manually(user_id, publication_dto, domain, authors_emails)

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
