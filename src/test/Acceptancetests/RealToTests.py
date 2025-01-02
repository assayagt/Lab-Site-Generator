from src.main.Util.Response import Response
from src.test.Acceptancetests.BridgeToTests import BridgeToTests
from src.main.DomainLayer.LabGenerator.GeneratorSystemService import GeneratorSystemService


class RealToTests(BridgeToTests):
    def __init__(self):
        self.generator_system_service = GeneratorSystemService.get_instance()

    def init(self):
        return self.generator_system_service.enter_generator_system()

    def enter_generator_system(self):
        return self.generator_system_service.enter_generator_system()

    def create_website(self, email, website_name, domain, components=None, template=None):
        return self.generator_system_service.create_website(email, website_name, domain, components, template)

    def change_website_name(self, new_name, domain):
        return self.generator_system_service.change_website_name(new_name, domain)

    def change_website_domain(self, email, new_domain, domain):
        return self.generator_system_service.change_website_domain(email, new_domain, domain)

    def change_website_template(self, domain, new_template=None):
        return self.generator_system_service.change_website_template(domain, new_template)

    def add_components_to_site(self, domain, new_components=None):
        return self.generator_system_service.add_components_to_site(domain, new_components)

    def login(self, user_id, email):
        return self.generator_system_service.login(user_id, email)

    def logout(self, user_id):
        return self.generator_system_service.logout(user_id)

    def get_logged_in_user(self):
        return self.generator_system_service.get_logged_in_user()
