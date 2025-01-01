from datetime import datetime
from src.main.DomainLayer.LabWebsites.WebCrawler.WebCrawlerFacade import WebCrawlerFacade
from src.main.DomainLayer.LabWebsites.Website.WebsiteFacade import WebsiteFacade
from src.main.DomainLayer.LabWebsites.Notifications.NotificationsFacade import NotificationsFacade
from src.main.DomainLayer.LabWebsites.User.AllWebsitesUserFacade import AllWebsitesUserFacade
from src.main.Util.ExceptionsEnum import ExceptionsEnum
class LabSystem:
    _singleton_instance = None

    def __init__(self):
        self.webCrawlerFacade = WebCrawlerFacade()
        self.websiteFacade = WebsiteFacade()
        self.notificationsFacade = NotificationsFacade()
        self.allWebsitesUserFacade = AllWebsitesUserFacade()

    @staticmethod
    def get_instance():
        if LabSystem._singleton_instance is None:
            LabSystem._singleton_instance = LabSystem()
        return LabSystem._singleton_instance

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        """
        Create a new lab website with the given domain, lab members, lab managers, and site creator
        """
        self.websiteFacade.create_new_website(domain)
        self.allWebsitesUserFacade.add_new_webstie_userFacade(domain)
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        for lab_member_email, lab_member_full_name in lab_members.items():
            userFacade.register_new_LabMember(lab_member_email, lab_member_full_name)
        for lab_manager_email, lab_manager_full_name in lab_managers.items():
            userFacade.create_new_site_manager(lab_manager_email, lab_manager_full_name)
        site_creator_email = site_creator.get("email")
        site_creator_full_name = site_creator.get("full_name")
        userFacade.set_site_creator(site_creator_email, site_creator_full_name)

    def login(self, domain, userId, email):
        """
        Login user into a specific website by email (should be via google in the future)
        If the given email is not associated with a member, an email is sent to all managers in order to approve\reject
        the registration request
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        member = userFacade.get_member_by_email(email)
        if member is None:
            self.send_registration_notification_to_all_LabManagers(domain, email)
        else:
            userFacade.login(userId, email)

    def send_registration_notification_to_all_LabManagers(self, domain, requestedEmail):
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        managers = userFacade.getManagers()
        for managerEmail in managers:
            self.notificationsFacade.send_registration_request_notification(requestedEmail, managerEmail)

    def logout(self, domain, userId):
        """
        Logout user from a specific website
        """
        self.allWebsitesUserFacade.logout(domain, userId)

    def create_new_site_manager_from_labWebsite(self, nominator_manager_userId, domain, nominated_manager_email):
        """
        Define and add new manager to a specific website, directly from the lab website.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        This operation can be done only by lab manager
        """
        self.allWebsitesUserFacade.create_new_site_manager_from_labWebsite(nominator_manager_userId, nominated_manager_email, domain)

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, lab_member_fullName, domain):
        """
        Define a new lab member in a specific website, directly from the lab website.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        This operation can be done only by lab manager
        """
        self.allWebsitesUserFacade.register_new_LabMember_from_labWebsite(manager_userId, email_to_register, lab_member_fullName, domain)

    def create_new_site_manager_from_generator(self, domain, nominated_manager_email):
        """
        Define and add new manager to a specific website, from generator site.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        """
        self.allWebsitesUserFacade.create_new_site_manager_from_generator(nominated_manager_email, domain)

    def register_new_LabMember_from_generator(self, email_to_register, lab_member_fullName, domain):
        """
        Define a new lab member in a specific website, from generator site.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        """
        self.allWebsitesUserFacade.register_new_LabMember_from_generator(email_to_register, lab_member_fullName, domain)

    def crawl_for_publications(self):
        """
        Fetches publications for the given authors and year from all WebCrawlers for all websites, and send
        notifications to authors for initial approve/disapprove.
        """
        # get list of all websites
        websites = self.websiteFacade.get_all_websites()

        # for each website, send to the webCrawler facade the members and current year to fetch publications
        for website in websites:
            websitePublications = self.webCrawlerFacade.fetch_publications(website.members, datetime.now().year)

            # check for each publication that is not already in website members publications
            for publication in websitePublications:
                if not website.check_publication_exist(publication):
                    authorsEmails = []
                    for author in publication.authors:
                        authorsEmails.append(self.allWebsitesUserFacade.getMemberEmailByName(author, website.domain))
                    website.create_publication(publication, authorsEmails)

                    # send notifications to the website authors about the new publications, for initial approve
                    for authorEmail in authorsEmails:
                        self.notificationsFacade.send_publication_notification(publication, authorEmail)

    def initial_approve_publication_by_author(self, userId, domain, publication_id):
        """
        Approve a publication by its author in the initial review stage.
        If the publication has not yet been final approved by a lab manager,
        the system sends a notification to lab managers requesting final approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
        if not self.websiteFacade.check_if_publication_approved(domain, publication_id):
            managers_emails = list(userFacade.getManagers().keys())
            for manager_email in managers_emails:
                publicationDTO = self.websiteFacade.get_publication_by_paper_id(domain, publication_id)
                self.notificationsFacade.send_publication_notification_for_final_approval(publicationDTO, manager_email)
        else:
            raise Exception(ExceptionsEnum.PUBLICATION_ALREADY_APPROVED.value)

    def final_approve_publication_by_manager(self, userId, domain, publication_id):
        """
        Approve a publication by a lab manager in the final review stage.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        userFacade.error_if_user_is_not_labManager(email, domain)
        self.websiteFacade.final_approve_publication(domain, publication_id)

    def add_publication_manually(self, userId, publicationDTO, domain, authors_emails):
        """A Lab Member updates the website with new research publications"""
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        userFacade.error_if_user_is_not_labMember_manager_creator(userId, domain)
        self.websiteFacade.create_new_publication(domain, publicationDTO, authors_emails)

    def get_all_approved_publication(self, domain):
        """
        return all approved publications of a specific website
        (in order to display them on the publication component of the website)
        """
        return self.websiteFacade.get_all_approved_publication(domain)

    def get_all_approved_publications_of_member(self, domain, email):
        """
        return all approved publications of a specific member of the lab website
        (in order to display them on his personal profile on the website)
        """
        return self.websiteFacade.get_all_approved_publications_of_member(domain, email)

    def define_member_as_alumni(self, manager_userId, member_email, domain):
        """
        define member (lab manager or lab member) as alumni
        Only managers can perform this operation.
        Site creator cant be defined as alumni.
        """
        return self.allWebsitesUserFacade.define_member_as_alumni(manager_userId, member_email, domain)

    def remove_manager_permission(self, manager_userId, manager_toRemove_email, domain):
        """A Lab Manager(manager_userId) removes the administrative permissions of another Lab Manager,
        reverting their role to a Lab Member.
        The permissions of the lab creator cannot be removed, it must always remain a Lab Manager"""
        return self.allWebsitesUserFacade.remove_manager_permission(manager_userId, manager_toRemove_email, domain)

    def get_all_alumnis(self, domain):
        return self.allWebsitesUserFacade.get_all_alumnis(domain)

    def get_all_lab_members(self, domain):
        return self.allWebsitesUserFacade.get_all_lab_members(domain)

    def get_all_lab_managers(self, domain):
        """notice! this function returns all managers including site creator!"""
        return self.get_all_lab_managers(domain)

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        self.allWebsitesUserFacade.set_secondEmail_by_member(userid, secondEmail, domain)

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        self.allWebsitesUserFacade.set_linkedin_link_by_member(userid, linkedin_link, domain)

    def set_media_by_member(self, userid, media, domain):
        self.allWebsitesUserFacade.set_media_by_member(userid, media, domain)

    def set_fullName_by_member(self, userid, fullName, domain):
        self.allWebsitesUserFacade.set_fullName_by_member(userid, fullName, domain)

    def set_degree_by_member(self, userid, degree, domain):
        self.allWebsitesUserFacade.set_degree_by_member(userid, degree, domain)

    def set_bio_by_member(self, userid, bio, domain):
        self.allWebsitesUserFacade.set_bio_by_member(userid, bio, domain)

    def set_publication_video_link(self, userId, domain, publication_id, video_link):
        """
        Set video link for a publication.
        - Authors can add video links, but it must be approved by a lab manager (the notification feature - in the future).
        - Lab managers can add video links directly without approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        if userFacade.verify_if_member_is_manager(email):
            self.websiteFacade.set_publication_video_link(domain, publication_id, video_link)
        else:
            self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
            self.websiteFacade.set_publication_video_link(domain, publication_id, video_link)
            #TODO: in the future, send notification to lab manager for approve

    def set_publication_git_link_by_author(self, userId, domain, publication_id, git_link):
        """
        Set git link for a publication.
        - Authors can add git links, but it must be approved by a lab manager (the notification feature - in the future).
        - Lab managers can add git links directly without approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        if userFacade.verify_if_member_is_manager(email):
            self.websiteFacade.set_publication_git_link(domain, publication_id, git_link)
        else:
            self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
            self.websiteFacade.set_publication_git_link(domain, publication_id, git_link)
            #TODO: in the future, send notification to lab manager for approve

    def set_publication_presentation_link_by_author(self, userId, domain, publication_id, presentation_link):
        """
        Set presentation link for a publication .
        - Authors can add presentation links, but it must be approved by a lab manager (the notification feature - in the future).
        - Lab managers can add presentation links directly without approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        if userFacade.verify_if_member_is_manager(email):
            self.websiteFacade.set_publication_presentation_link(domain, publication_id, presentation_link)
        else:
            self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
            self.websiteFacade.set_publication_presentation_link(domain, publication_id, presentation_link)
            #TODO: in the future, send notification to lab manager for approve



