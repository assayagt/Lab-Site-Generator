from src.main.DomainLayer.LabGenerator.User.UserFacade import UserFacade
from src.main.DomainLayer.LabWebsites.LabSystem.LabSystem import LabSystem

class GeneratorSystem:
    _singleton_instance = None

    def __init__(self):
        self.user_facade = UserFacade()
        self.labSystem = LabSystem()

    @staticmethod
    def get_instance():
        if GeneratorSystem._singleton_instance is None:
            GeneratorSystem._singleton_instance = GeneratorSystem()
        return GeneratorSystem._singleton_instance

    def login(self, userId, email):
        """
        login into the generator system  (should be via google in the future).
        A user can log in to the generator system using any email address of their choice.
        """
        self.user_facade.error_if_user_notExist(userId)
        self.user_facade.login(userId, email)

    def logout(self, userId):
        """
        logout from the generator system (should be via google in the future)
        """
        self.user_facade.error_if_user_notExist(userId)
        self.user_facade.logout(userId)

    def create_new_lab_website(self, domain, lab_members_emails, lab_managers_emails, site_creator_email):
        """
        Generates a new lab website once the custom site configuration is complete.
        """
        self.labSystem.create_new_lab_website(domain, lab_members_emails, lab_managers_emails, site_creator_email)

    def create_new_site_manager(self, email, domain):
        """
        Define and add new manager to a specific website, from generator site.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        """
        self.user_facade.create_new_site_manager(email, domain)
        self.labSystem.create_new_site_manager_from_generator(domain, email)

    def register_new_LabMember_from_generator(self, email_to_register, domain):
        """
        Define a new lab member in a specific website, from generator site.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        """
        self.labSystem.register_new_LabMember_from_generator(email_to_register, domain)

