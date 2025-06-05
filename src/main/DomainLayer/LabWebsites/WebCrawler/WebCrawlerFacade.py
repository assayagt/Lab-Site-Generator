import threading
import time
from queue import Queue
from concurrent.futures import Future
from typing import Any
from src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler import GoogleScholarWebCrawler
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO

class _CrawlTask:
    __slots__ = ("kind", "payload", "future")
    def __init__(self, kind: str, payload: Any, future: Future):
        # kind is either "fetch" of "fill"
        self.kind=kind
        self.payload=payload
        self.future=future

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
        self._tasks = Queue()
        t = threading.Thread(target=self._worker_loop, daemon=True)
        t.start()
        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (useful for unit tests)."""
        with cls._instance_lock:
            cls._instance = None

    def fetch_async(self, scholar_links) -> Future:
        """
        Schedule a fetch_publications job.
        Future.result() will be List[PublicationDTO].
        """
        fut = Future()
        self._tasks.put(_CrawlTask("fetch", scholar_links, fut))
        return fut
    
    def fill_async(self, pubs) -> Future:
        """
        Schedule a fill_details job.
        Future.result() will be the same List[PublicationDTO] mutated in-place.
        """
        fut = Future()
        self._tasks.put(_CrawlTask("fill", pubs, fut))
        return fut
    
    def _worker_loop(self):
        """
        Single thread: process one task every 30 seconds.
        """
        while True:
            task: _CrawlTask = self._tasks.get()
            try:
                if task.kind == "fetch":
                    # run fetch
                    pubs = self.fetch_publications(task.payload)
                    task.future.set_result(pubs)

                elif task.kind == "fill":
                    # run fill (in-place)
                    self.fill_pub_details(task.payload)
                    task.future.set_result(task.payload)
                else:
                    raise ValueError(f"Unknown task kind: {task.kind}")
            except Exception as e:
                task.future.set_exception(e)
            time.sleep(30)


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
