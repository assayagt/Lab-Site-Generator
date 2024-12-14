from abc import ABC, abstractmethod

class WebCrawler(ABC):
    @abstractmethod
    def fetch_crawler_publications(self, authors, date):
        """
        Abstract method to fetch publications for the given authors and date.
        Must be implemented by concrete crawlers.
        """
        pass
