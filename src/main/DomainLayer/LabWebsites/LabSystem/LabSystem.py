from datetime import datetime
from src.main.DomainLayer.LabWebsites.WebCrawler.WebCrawlerFacade import WebCrawlerFacade
from src.main.DomainLayer.LabWebsites.Website.WebsiteFacade import WebsiteFacade
from src.main.DomainLayer.LabWebsites.Notifications.NotificationsFacade import NotificationsFacade
from src.main.DomainLayer.LabWebsites.User.AllWebsitesUserFacade import AllWebsitesUserFacade
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

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, domain):
        """
        Define a new lab member in a specific website, directly from the lab website.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        This operation can be done only by lab manager
        """
        self.allWebsitesUserFacade.register_new_LabMember_from_labWebsite(manager_userId, email_to_register, domain)

    def create_new_site_manager_from_generator(self, domain, nominated_manager_email):
        """
        Define and add new manager to a specific website, during site creation or from generator site.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        """
        self.allWebsitesUserFacade.create_new_site_manager_from_generator(nominated_manager_email, domain)

    def register_new_LabMember_from_generator(self, email_to_register, domain):
        """
        Define a new lab member in a specific website, during site creation or from generator site.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        """
        self.allWebsitesUserFacade.register_new_LabMember_from_generator(email_to_register, domain)

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
                    website.create_publication(publication.title, publication.authors, publication.date,
                                               publication.approved, publication.publication_link, publication.media, authorsEmails)

                    # send notifications to the website authors about the new publications, for initial approve
                    for authorEmail in authorsEmails:
                        self.notificationsFacade.send_publication_notification(publication, authorEmail)

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



