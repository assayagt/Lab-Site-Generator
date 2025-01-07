from src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler import GoogleScholarWebCrawler


class WebCrawlerFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebCrawlerFacade, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.web_crawlers = [GoogleScholarWebCrawler()]  # Holds all WebCrawler instances
            self._initialized = True


    def fetch_publications(self, authors, year):
        """
        Calls fetch_crawler_publications on each WebCrawler.
        """
        all_results = []
        for crawler in self.web_crawlers:
            results = crawler.fetch_crawler_publications(authors, year)
            all_results.extend(results)
        return all_results
