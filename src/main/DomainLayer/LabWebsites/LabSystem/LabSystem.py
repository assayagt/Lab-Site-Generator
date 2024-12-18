from datetime import datetime
from src.main.DomainLayer.LabWebsites.WebCrawler import WebCrawlerFacade
from src.main.DomainLayer.LabWebsites.Website import WebsiteFacade
from src.main.DomainLayer.LabWebsites.Notifications import NotificationsFacade

class LabSystem:
    _singleton_instance = None

    def __init__(self):
        self.webCrawlerFacade = WebCrawlerFacade()
        self.websiteFacade = WebsiteFacade()
        self.notificationsFacade = NotificationsFacade()

    @staticmethod
    def get_instance():
        if LabSystem._singleton_instance is None:
            LabSystem._singleton_instance = LabSystem()
        return LabSystem._singleton_instance

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

            #TODO: send notifications to the website members about the new publications





