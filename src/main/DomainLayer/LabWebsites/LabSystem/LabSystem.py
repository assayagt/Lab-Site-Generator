class LabSystem:
    _singleton_instance = None

    def __init__(self):
        if LabSystem._singleton_instance is not None:
            raise Exception("This is a singleton class!")

    @staticmethod
    def get_instance():
        if LabSystem._singleton_instance is None:
            LabSystem._singleton_instance = LabSystem()
        return LabSystem._singleton_instance

    def crawl_for_publications(self):
        """
        Fetches publications for the given authors and year from all WebCrawlers.
        """
        #call the WebCrawlerFacade to fetch publications
        WebCrawlerFacade().fetch_publications()

        #TODO: Send notifications to the website members about the new publications





