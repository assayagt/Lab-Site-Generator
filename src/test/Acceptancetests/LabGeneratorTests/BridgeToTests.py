from abc import ABC, abstractmethod

class BridgeToTests(ABC):
    @abstractmethod
    def enter_generator_system(self):
        pass

    def get_lab_system_controller(self):
        pass

    @abstractmethod
    def create_website(self, email, website_name, domain, components, template):
        pass

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        pass

    @abstractmethod
    def change_website_name(self, userId, new_name, domain):
        pass

    @abstractmethod
    def change_website_domain(self, userId, new_domain, domain):
        pass

    @abstractmethod
    def change_website_template(self, userId, domain, new_template=None):
        pass

    @abstractmethod
    def add_components_to_site(self, userId, domain, new_components):
        pass

    def create_new_site_manager(self, nominator_manager_userId, nominated_manager_email, domain):
        pass

    def register_new_LabMember_from_generator(self, manager_userId, email_to_register, lab_member_fullName, lab_member_degree, domain):
        pass

    @abstractmethod
    def login(self, user_id, email):
        pass

    @abstractmethod
    def logout(self, user_id):
        pass

    @abstractmethod
    def get_logged_in_user(self):
        pass

    @abstractmethod
    def get_site_by_domain(self, domain):
        pass

    def reset_system(self):
        pass

    @abstractmethod
    def change_site_logo_by_manager(self, user_id, domain):
        pass

    @abstractmethod
    def remove_site_manager_from_generator(self, nominator_manager_userId, manager_toRemove_email, domain):
        pass

    @abstractmethod
    def add_alumni_from_generator(self, manager_userId, email_toSetAlumni, domain):
        pass

    @abstractmethod
    def remove_alumni_from_generator(self, manager_userId, email_toRemoveAlumni, domain):
        pass

    @abstractmethod
    def add_alumni_from_lab_website(self, email_toSetAlumni, domain):
        pass

    @abstractmethod
    def change_site_home_picture_by_manager(self, user_id, domain):
        pass

    @abstractmethod
    def create_new_site_manager_from_lab_website(self, nominated_manager_email, domain):
        pass

    @abstractmethod
    def get_all_custom_websites_of_manager(self, user_id):
        pass

    @abstractmethod
    def get_custom_website(self, user_id, domain):
        pass

    @abstractmethod
    def set_site_about_us_by_manager_from_generator(self, user_id, domain, about_us):
        pass

    @abstractmethod
    def set_site_about_us_on_creation_from_generator(self, domain, about_us):
        pass

    @abstractmethod
    def set_site_contact_info_by_manager_from_generator(self, user_id, domain, contact_info_dto):
        pass

    @abstractmethod
    def set_site_contact_info_on_creation_from_generator(self, domain, contact_info_dto):
        pass

    @abstractmethod
    def site_creator_resignation_from_generator(self, site_creator_user_id, domain, nominated_email, new_role):
        pass

    @abstractmethod
    def site_creator_resignation_from_lab_website(self, domain, nominated_email, new_role):
        pass