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
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.logout(userId)

    def create_new_site_manager(self, domain, email):
        """
        Define and add new manager to a specific website.
        The given email must be associated with a Lab Member of the given website
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_labMember_notExist(email)
        userFacade.create_new_site_manager(email)

    def register_new_LabMember(self, domain, email):
        """
        Define a new lab member in a specific website.
        The given email must not be associated with a member(manager/lab member/creator..) of the given website
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.register_new_LabMember(email)

    def crawl_for_publications(self):
        """
        Fetches publications for the given authors and year from all WebCrawlers for all websites.
        """
        # get list of all websites
        websites = self.websiteFacade.get_all_websites()

        # for each website, send to the webCrawler facade the members and current year to fetch publications
        publications = []
        for website in websites:
            websitePublications = self.webCrawlerFacade.fetch_publications(website.members, datetime.now().year)

            # check for each publication that is not already in website members publications
            for publication in websitePublications:
                if not website.check_publication_exist(publication):
                    publications.append(publication)

                    # send notifications to the website authors about the new publications, for initial approve
                    authors = publication.authors
                    for author in authors:
                        email = self.allWebsitesUserFacade.getMemberEmailByName(author, website.domain)
                        self.notificationsFacade.send_publication_notification(publication, email)





