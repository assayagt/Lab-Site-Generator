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

    def add_publication_manually(self, user_id, publication_dto, domain, authors_emails):
        if self.real_service_adapter:
            return self.real_service_adapter.add_publication_manually(user_id, publication_dto, domain, authors_emails)
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
