class WebCrawlerFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebCrawlerFacade, cls).__new__(cls)
        return cls._instance

    def fetch_publications(self, authors, date):
        pass
