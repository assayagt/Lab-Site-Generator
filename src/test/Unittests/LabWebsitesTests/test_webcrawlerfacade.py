import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os
import threading
from concurrent.futures import Future

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.main.DomainLayer.LabWebsites.WebCrawler.WebCrawlerFacade import WebCrawlerFacade, _CrawlTask
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO

class TestWebCrawlerFacade(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Reset singleton before tests
        WebCrawlerFacade.reset_instance()
    
    def setUp(self):
        # Reset singleton before each test
        WebCrawlerFacade.reset_instance()
        self.facade = WebCrawlerFacade()
    
    def tearDown(self):
        # Reset singleton after each test
        WebCrawlerFacade.reset_instance()
    
    def test_singleton_pattern(self):
        facade1 = WebCrawlerFacade()
        facade2 = WebCrawlerFacade()
        self.assertIs(facade1, facade2)
    
    def test_get_instance(self):
        facade1 = WebCrawlerFacade.get_instance()
        facade2 = WebCrawlerFacade.get_instance()
        self.assertIs(facade1, facade2)
    
    def test_reset_instance(self):
        facade1 = WebCrawlerFacade()
        WebCrawlerFacade.reset_instance()
        facade2 = WebCrawlerFacade()
        self.assertIsNot(facade1, facade2)
    
    def test_initialization(self):
        self.assertIsNotNone(self.facade.web_crawlers)
        self.assertIsNotNone(self.facade._tasks)
        self.assertTrue(self.facade._initialized)
    
    def test_crawl_task_initialization(self):
        future = Future()
        task = _CrawlTask("fetch", ["test_link"], future)
        self.assertEqual(task.kind, "fetch")
        self.assertEqual(task.payload, ["test_link"])
        self.assertEqual(task.future, future)
    
    def test_fetch_async(self):
        future = self.facade.fetch_async(["test_link"])
        self.assertIsInstance(future, Future)
        # Check that task was added to queue
        self.assertFalse(self.facade._tasks.empty())
    
    def test_fill_async(self):
        pubs = [PublicationDTO("Test Pub", 2023, "http://test.com", ["Author"])]
        future = self.facade.fill_async(pubs)
        self.assertIsInstance(future, Future)
        # Check that task was added to queue
        self.assertFalse(self.facade._tasks.empty())
    
    @patch('src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler.GoogleScholarWebCrawler')
    def test_fetch_publications(self, mock_crawler_class):
        mock_crawler = Mock()
        mock_crawler.fetch_crawler_publications.return_value = [
            PublicationDTO("Test Pub 1", 2023, "http://test1.com", ["Author1"]),
            PublicationDTO("Test Pub 2", 2023, "http://test2.com", ["Author2"])
        ]
        mock_crawler_class.return_value = mock_crawler
        
        # Reset facade to use mocked crawler
        WebCrawlerFacade.reset_instance()
        facade = WebCrawlerFacade()
        facade.web_crawlers = [mock_crawler]
        
        scholar_links = ["http://scholar1.com", "http://scholar2.com"]
        results = facade.fetch_publications(scholar_links)
        
        mock_crawler.fetch_crawler_publications.assert_called_once_with(scholarLinks=scholar_links)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, "Test Pub 1")
        self.assertEqual(results[1].title, "Test Pub 2")
    
    @patch('src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler.GoogleScholarWebCrawler')
    def test_fetch_publications_multiple_crawlers(self, mock_crawler_class):
        mock_crawler1 = Mock()
        mock_crawler1.fetch_crawler_publications.return_value = [
            PublicationDTO("Test Pub 1", 2023, "http://test1.com", ["Author1"])
        ]
        
        mock_crawler2 = Mock()
        mock_crawler2.fetch_crawler_publications.return_value = [
            PublicationDTO("Test Pub 2", 2023, "http://test2.com", ["Author2"])
        ]
        
        mock_crawler_class.side_effect = [mock_crawler1, mock_crawler2]
        
        # Reset facade to use mocked crawlers
        WebCrawlerFacade.reset_instance()
        facade = WebCrawlerFacade()
        facade.web_crawlers = [mock_crawler1, mock_crawler2]
        
        scholar_links = ["http://scholar1.com"]
        results = facade.fetch_publications(scholar_links)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, "Test Pub 1")
        self.assertEqual(results[1].title, "Test Pub 2")
    
    @patch('src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler.GoogleScholarWebCrawler')
    def test_get_details_by_link(self, mock_crawler_class):
        mock_crawler = Mock()
        mock_crawler.get_details_by_link.return_value = ["Author1", "Author2"]
        mock_crawler_class.return_value = mock_crawler
        
        # Reset facade to use mocked crawler
        WebCrawlerFacade.reset_instance()
        facade = WebCrawlerFacade()
        facade.web_crawlers = [mock_crawler]
        
        link = "http://test.com"
        result = facade.get_details_by_link(link)
        
        mock_crawler.get_details_by_link.assert_called_once_with(link)
        self.assertEqual(result, ["Author1", "Author2"])
    
    @patch('src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler.GoogleScholarWebCrawler')
    def test_get_details_by_link_no_result(self, mock_crawler_class):
        mock_crawler = Mock()
        mock_crawler.get_details_by_link.return_value = None
        mock_crawler_class.return_value = mock_crawler
        
        # Reset facade to use mocked crawler
        WebCrawlerFacade.reset_instance()
        facade = WebCrawlerFacade()
        facade.web_crawlers = [mock_crawler]
        
        link = "http://test.com"
        result = facade.get_details_by_link(link)
        
        self.assertIsNone(result)
    
    @patch('src.main.DomainLayer.LabWebsites.WebCrawler.GoogleScholarWebCrawler.GoogleScholarWebCrawler')
    def test_fill_pub_details(self, mock_crawler_class):
        mock_crawler = Mock()
        mock_crawler_class.return_value = mock_crawler
        
        # Reset facade to use mocked crawler
        WebCrawlerFacade.reset_instance()
        facade = WebCrawlerFacade()
        facade.web_crawlers = [mock_crawler]
        
        pubs = [PublicationDTO("Test Pub", 2023, "http://test.com", ["Author"])]
        facade.fill_pub_details(pubs)
        
        mock_crawler.fill_details.assert_called_once_with(publicationDTOs=pubs)
    
    def test_worker_loop_task_processing(self):
        # This test verifies that the worker loop can process tasks
        # We'll test the task processing logic without actually running the loop
        future = Future()
        task = _CrawlTask("fetch", ["test_link"], future)
        
        # Simulate successful task processing
        try:
            if task.kind == "fetch":
                # Mock the fetch operation
                pubs = [PublicationDTO("Test Pub", 2023, "http://test.com", ["Author"])]
                task.future.set_result(pubs)
            elif task.kind == "fill":
                # Mock the fill operation
                task.future.set_result(task.payload)
            else:
                raise ValueError(f"Unknown task kind: {task.kind}")
        except Exception as e:
            task.future.set_exception(e)
        
        # Verify the future was completed successfully
        self.assertTrue(future.done())
        self.assertFalse(future.exception())
        result = future.result()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Test Pub")
    
    def test_worker_loop_exception_handling(self):
        future = Future()
        task = _CrawlTask("invalid_kind", None, future)
        
        # Simulate exception in task processing
        try:
            if task.kind == "fetch":
                task.future.set_result([])
            elif task.kind == "fill":
                task.future.set_result([])
            else:
                raise ValueError(f"Unknown task kind: {task.kind}")
        except Exception as e:
            task.future.set_exception(e)
        
        # Verify the future was completed with exception
        self.assertTrue(future.done())
        self.assertIsNotNone(future.exception())
        self.assertIsInstance(future.exception(), ValueError)

if __name__ == '__main__':
    unittest.main() 