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

    def create_website(self, userId, website_name, domain, components=None, template=None):
        if self.real_service_adapter:
            return self.real_service_adapter.create_website(userId, website_name, domain, components, template)
        return Response(None, "Not Implemented yet")

    def change_website_name(self, userId, new_name, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.change_website_name(userId, new_name, domain)
        return Response(None, "Not Implemented yet")

    def change_website_domain(self, email, new_domain, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.change_website_domain(email, new_domain, domain)
        return Response(None, "Not Implemented yet")

    def change_website_template(self, domain, new_template=None):
        if self.real_service_adapter:
            return self.real_service_adapter.change_website_template(domain, new_template)
        return Response(None, "Not Implemented yet")

    def add_components_to_site(self, domain, new_components=None):
        if self.real_service_adapter:
            return self.real_service_adapter.add_components_to_site(domain, new_components)
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
