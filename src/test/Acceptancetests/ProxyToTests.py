from src.test.Acceptancetests.BridgeToTests import BridgeToTests
from src.test.Acceptancetests.RealToTests import RealToTests
from src.main.Util.Response import Response


class ProxyToTest(BridgeToTests):
    def __init__(self, type):
        if type == "Real":
            self.real_service_adapter = RealToTests()
        else:
            self.real_service_adapter = None

    def enter_generator_system(self):
        if self.real_service_adapter:
            return self.real_service_adapter.enter_generator_system()
        return Response(None, "Not Implemented yet")

    def create_website(self, userId, website_name, domain, components, template):
        if self.real_service_adapter:
            return self.real_service_adapter.create_website(userId, website_name, domain, components, template)
        return Response(None, "Not Implemented yet")

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        if self.real_service_adapter:
            return self.real_service_adapter.create_new_lab_website(domain, lab_members, lab_managers, site_creator)
        return Response(None, "Not Implemented yet")

    def change_website_name(self, userId, new_name, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.change_website_name(userId, new_name, domain)
        return Response(None, "Not Implemented yet")

    def change_website_domain(self, userId, new_domain, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.change_website_domain(userId, new_domain, domain)
        return Response(None, "Not Implemented yet")

    def change_website_template(self, userId, domain, new_template=None):
        if self.real_service_adapter:
            return self.real_service_adapter.change_website_template(userId, domain, new_template)
        return Response(None, "Not Implemented yet")

    def add_components_to_site(self, userId, domain, new_components):
        if self.real_service_adapter:
            return self.real_service_adapter.add_components_to_site(userId, domain, new_components)
        return Response(None, "Not Implemented yet")

    def create_new_site_manager(self, nominator_manager_userId, nominated_manager_email, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.create_new_site_manager(nominator_manager_userId, nominated_manager_email, domain)
        return Response(None, "Not Implemented yet")

    def register_new_LabMember_from_generator(self, manager_userId, email_to_register, lab_member_fullName, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.register_new_LabMember_from_generator(manager_userId, email_to_register, lab_member_fullName, domain)
        return Response(None, "Not Implemented yet")

    def login(self, user_id, email):
        if self.real_service_adapter:
            return self.real_service_adapter.login(user_id, email)
        return Response(None, "Not Implemented yet")

    def logout(self, user_id):
        if self.real_service_adapter:
            return self.real_service_adapter.logout(user_id)
        return Response(None, "Not Implemented yet")

    def get_logged_in_user(self):
        if self.real_service_adapter:
            return self.real_service_adapter.get_logged_in_user()
        return Response(None, "Not Implemented yet")

    def reset_system(self):
        if self.real_service_adapter:
            return self.real_service_adapter.reset_system()
        return Response(None, "Not Implemented yet")