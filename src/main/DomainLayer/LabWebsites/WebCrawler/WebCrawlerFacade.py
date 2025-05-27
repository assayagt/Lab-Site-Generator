import threading

from src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler import GoogleScholarWebCrawler
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO

class WebCrawlerFacade:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(WebCrawlerFacade, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.web_crawlers = [GoogleScholarWebCrawler()]  # Holds all WebCrawler instances
        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (useful for unit tests)."""
        with cls._instance_lock:
            cls._instance = None


    def fetch_publications(self, scholar_links)-> list[PublicationDTO]: #=================================== refactored
        """
        Calls fetch_crawler_publications on each WebCrawler.
        """
        all_results = []
        for crawler in self.web_crawlers:
            results = crawler.fetch_crawler_publications(scholarLinks=scholar_links)
            all_results.extend(results)
        return all_results

    def get_details_by_link(self, link):
        """
        Calls get_authors_by_link on each WebCrawler.
        """
        for crawler in self.web_crawlers:
            authors = crawler.get_details_by_link(link)
            if authors:
                return authors
        return None

    def fill_pub_details(self, pubDTOs: list[PublicationDTO]): # should be refactored to work with other crawlers
        """
            Calls getPublicationDTOs on each WebCrawler.
        """
        for crawler in self.web_crawlers:
            crawler.fill_details(publicationDTOs=pubDTOs)
