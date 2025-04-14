from src.test.Acceptancetests.LabGeneratorTests.BridgeToTests import BridgeToTests
from src.test.Acceptancetests.LabGeneratorTests.RealToTests import RealToTests
from src.main.Util.Response import Response


class ProxyToTest(BridgeToTests):
    def __init__(self, type):
        if type == "Real":
            self.real_service_adapter = RealToTests()
        else:
            self.real_service_adapter = None

    def get_lab_system_controller(self):
        if self.real_service_adapter:
            return self.real_service_adapter.get_lab_system_controller()
        return Response(None, "Not Implemented yet")

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

    def register_new_LabMember_from_generator(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.register_new_LabMember_from_generator(manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain)
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

    def get_site_by_domain(self, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.get_site_by_domain(domain)
        return Response(None, "Not Implemented yet")

    def change_site_logo_by_manager(self, user_id, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.change_site_logo_by_manager(user_id, domain)
        return Response(None, "Not Implemented yet")

    def remove_site_manager_from_generator(self, nominator_manager_userId, manager_toRemove_email, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.remove_site_manager_from_generator(nominator_manager_userId, manager_toRemove_email, domain)
        return Response(None, "Not Implemented yet")

    def add_alumni_from_generator(self, manager_userId, email_toSetAlumni, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.add_alumni_from_generator(manager_userId, email_toSetAlumni, domain)
        return Response(None, "Not Implemented yet")

    def remove_alumni_from_generator(self, manager_userId, email_toRemoveAlumni, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.remove_alumni_from_generator(manager_userId, email_toRemoveAlumni, domain)
        return Response(None, "Not Implemented yet")

    def add_alumni_from_lab_website(self, email_toSetAlumni, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.add_alumni_from_lab_website(email_toSetAlumni, domain)
        return Response(None, "Not Implemented yet")

    def change_site_home_picture_by_manager(self, user_id, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.change_site_home_picture_by_manager(user_id, domain)
        return Response(None, "Not Implemented yet")

    def create_new_site_manager_from_lab_website(self, nominated_manager_email, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.create_new_site_manager_from_lab_website(nominated_manager_email, domain)
        return Response(None, "Not Implemented yet")

    def get_all_custom_websites_of_manager(self, user_id):
        if self.real_service_adapter:
            return self.real_service_adapter.get_all_custom_websites_of_manager(user_id)
        return Response(None, "Not Implemented yet")

    def get_custom_website(self, user_id, domain):
        if self.real_service_adapter:
            return self.real_service_adapter.get_custom_website(user_id, domain)
        return Response(None, "Not Implemented yet")

    def set_site_about_us_by_manager_from_generator(self, user_id, domain, about_us):
        if self.real_service_adapter:
            return self.real_service_adapter.set_site_about_us_by_manager_from_generator(user_id, domain, about_us)
        return Response(None, "Not Implemented yet")

    def set_site_about_us_on_creation_from_generator(self, domain, about_us):
        if self.real_service_adapter:
            return self.real_service_adapter.set_site_about_us_on_creation_from_generator(domain, about_us)
        return Response(None, "Not Implemented yet")

    def set_site_contact_info_by_manager_from_generator(self, user_id, domain, contact_info_dto):
        if self.real_service_adapter:
            return self.real_service_adapter.set_site_contact_info_by_manager_from_generator(user_id, domain,
                                                                                             contact_info_dto)
        return Response(None, "Not Implemented yet")

    def set_site_contact_info_on_creation_from_generator(self, domain, contact_info_dto):
        if self.real_service_adapter:
            return self.real_service_adapter.set_site_contact_info_on_creation_from_generator(domain, contact_info_dto)
        return Response(None, "Not Implemented yet")

    def site_creator_resignation_from_generator(self, site_creator_user_id, domain, nominated_email, new_role):
        if self.real_service_adapter:
            return self.real_service_adapter.site_creator_resignation_from_generator(site_creator_user_id, domain,
                                                                                     nominated_email, new_role)
        return Response(None, "Not Implemented yet")

    def site_creator_resignation_from_lab_website(self, domain, nominated_email, new_role):
        if self.real_service_adapter:
            return self.real_service_adapter.site_creator_resignation_from_lab_website(domain, nominated_email,
                                                                                       new_role)
        return Response(None, "Not Implemented yet")