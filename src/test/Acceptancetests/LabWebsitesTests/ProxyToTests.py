from src.test.Acceptancetests.LabWebsitesTests.BridgeToTests import BridgeToTests
from src.test.Acceptancetests.LabWebsitesTests.RealToTests import RealToTests
from src.main.Util.Response import Response


class ProxyToTests(BridgeToTests):
    def __init__(self, service_type, lab_system_controller):
        if service_type == "Real":
            self.real_service_adapter = RealToTests(lab_system_controller)
        else:
            self.real_service_adapter = None

    def enter_lab_website(self, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.enter_lab_website(domain)
        return Response(None, "Not Implemented yet")

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        if self.real_service_adapter:
            return self.real_service_adapter.create_new_lab_website(domain, lab_members, lab_managers, site_creator)
        return Response(None, "Not Implemented yet")

    def login(self, domain, user_id, email):
        if self.real_service_adapter:
            return self.real_service_adapter.login(domain, user_id, email)
        return Response(None, "Not Implemented yet")

    def logout(self, domain, user_id):
        if self.real_service_adapter:
            return self.real_service_adapter.logout(domain, user_id)
        return Response(None, "Not Implemented yet")

    def crawl_for_publications(self):
        if self.real_service_adapter:
            return self.real_service_adapter.crawl_for_publications()
        return Response(None, "Not Implemented yet")

    def initial_approve_publication_by_author(self, user_id, domain, publication_id):
        if self.real_service_adapter:
            return self.real_service_adapter.initial_approve_publication_by_author(user_id, domain, publication_id)
        return Response(None, "Not Implemented yet")

    def final_approve_publication_by_manager(self, user_id, domain, publication_id):
        if self.real_service_adapter:
            return self.real_service_adapter.final_approve_publication_by_manager(user_id, domain, publication_id)
        return Response(None, "Not Implemented yet")

    def add_publication_manually(self, user_id, domain, publication_link, git_link, video_link, presentation_link):
        if self.real_service_adapter:
            return self.real_service_adapter.add_publication_manually(user_id, domain, publication_link, git_link, video_link, presentation_link)
        return Response(None, "Not Implemented yet")

    def get_all_approved_publications(self, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.get_all_approved_publications(domain)
        return Response(None, "Not Implemented yet")

    def get_all_approved_publications_of_member(self, domain, email):
        if self.real_service_adapter:
            return self.real_service_adapter.get_all_approved_publications_of_member(domain, email)
        return Response(None, "Not Implemented yet")

    def set_publication_video_link(self, user_id, domain, publication_id, video_link):
        if self.real_service_adapter:
            return self.real_service_adapter.set_publication_video_link(user_id, domain, publication_id, video_link)
        return Response(None, "Not Implemented yet")

    def set_publication_git_link(self, user_id, domain, publication_id, git_link):
        if self.real_service_adapter:
            return self.real_service_adapter.set_publication_git_link(user_id, domain, publication_id, git_link)
        return Response(None, "Not Implemented yet")

    def set_publication_presentation_link(self, user_id, domain, publication_id, presentation_link):
        if self.real_service_adapter:
            return self.real_service_adapter.set_publication_presentation_link(user_id, domain, publication_id, presentation_link)
        return Response(None, "Not Implemented yet")

    def define_member_as_alumni(self, manager_user_id, member_email, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.define_member_as_alumni(manager_user_id, member_email, domain)
        return Response(None, "Not Implemented yet")

    def remove_manager_permission(self, manager_user_id, manager_to_remove_email, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.remove_manager_permission(manager_user_id, manager_to_remove_email, domain)
        return Response(None, "Not Implemented yet")

    def approve_registration_request(self, domain, manager_userId, requested_email, requested_full_name, requested_degree):
        if self.real_service_adapter:
            return self.real_service_adapter.approve_registration_request(domain, manager_userId, requested_email, requested_full_name, requested_degree)
        return Response(None, "Not Implemented yet")

    def reject_registration_request(self, domain, manager_userId, requested_email):
        if self.real_service_adapter:
            return self.real_service_adapter.reject_registration_request(domain, manager_userId, requested_email)
        return Response(None, "Not Implemented yet")

    def create_new_site_manager_from_labWebsite(self, nominator_manager_userId, domain, nominated_manager_email):
        if self.real_service_adapter:
            return self.real_service_adapter.create_new_site_manager_from_labWebsite(nominator_manager_userId, domain, nominated_manager_email)
        return Response(None, "Not Implemented yet")

    def get_all_lab_managers(self, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.get_all_lab_managers(domain)
        return Response(None, "Not Implemented yet")

    def get_all_lab_members(self, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.get_all_lab_members(domain)
        return Response(None, "Not Implemented yet")

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.register_new_LabMember_from_labWebsite(manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain)
        return Response(None, "Not Implemented yet")

    def get_all_alumnis(self, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.get_all_alumnis(domain)
        return Response(None, "Not Implemented yet")

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.set_secondEmail_by_member(userid, secondEmail, domain)
        return Response(None, "Not Implemented yet")

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.set_linkedin_link_by_member(userid, linkedin_link, domain)
        return Response(None, "Not Implemented yet")

    def set_fullName_by_member(self, userid, fullName, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.set_fullName_by_member(userid, fullName, domain)
        return Response(None, "Not Implemented yet")

    def set_degree_by_member(self, userid, degree, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.set_degree_by_member(userid, degree, domain)
        return Response(None, "Not Implemented yet")

    def set_bio_by_member(self, userid, bio, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.set_bio_by_member(userid, bio, domain)
        return Response(None, "Not Implemented yet")

    def set_media_by_member(self, userid, media, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.set_media_by_member(userid, media, domain)
        return Response(None, "Not Implemented yet")

    def get_all_lab_members_details(self, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.get_all_lab_members_details(domain)
        return Response(None, "Not Implemented yet")