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

    def create_website(self, email, website_name, domain, components, template):
        return self.generator_system_service.create_website(email, website_name, domain, components, template)

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        return self.generator_system_service.create_new_lab_website(domain, lab_members, lab_managers, site_creator)

    def change_website_name(self, userId, new_name, domain):
        return self.generator_system_service.change_website_name(userId, new_name, domain)

    def change_website_domain(self, userId, new_domain, domain):
        return self.generator_system_service.change_website_domain(userId, new_domain, domain)

    def change_website_template(self, userId, domain, new_template=None):
        return self.generator_system_service.change_website_template(userId, domain, new_template)

    def add_components_to_site(self, userId, domain, new_components):
        return self.generator_system_service.add_components_to_site(userId, domain, new_components)

    def login(self, user_id, email):
        return self.generator_system_service.login(user_id, email)

    def logout(self, user_id):
        return self.generator_system_service.logout(user_id)

    def get_logged_in_user(self):
        return self.generator_system_service.get_logged_in_user()

    def reset_system(self):
        return self.generator_system_service.reset_system()