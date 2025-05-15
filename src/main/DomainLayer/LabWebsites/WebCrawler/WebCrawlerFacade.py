import threading

from src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler import GoogleScholarWebCrawler


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


    def fetch_publications(self, scholar_links, domain): #=================================== refactored
        """
        Calls fetch_crawler_publications on each WebCrawler.
        """
        all_results = []
        for crawler in self.web_crawlers:
            results = crawler.fetch_crawler_publications(scholarLinks=scholar_links, domain=domain)
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

    def get_PublicationDTOs(self, scannedPub_keys: list[tuple[str, str]]): #===================================
        """
            Calls getPublicationDTOs on each WebCrawler.
        """
        for crawler in self.web_crawlers:
            crawler.getPublicationDTOs(scannedPub_keys)

    def fetch_publications_new_member(self, scholar_ids, domain): #TODO: reduntant function can be removed later
        """
        Calls fetch_publications_new_member on each WebCrawler.
        """
        for crawler in self.web_crawlers:
            crawler.fetch_crawler_publications(scholar_ids=scholar_ids, domain=domain)
