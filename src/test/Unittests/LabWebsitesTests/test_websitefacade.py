import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os
import uuid
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.main.DomainLayer.LabWebsites.Website.WebsiteFacade import WebsiteFacade
from src.main.DomainLayer.LabWebsites.Website.Website import Website
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.DomainLayer.LabWebsites.Website.ContactInfo import ContactInfo
from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.DAL.DTOs.NewsRecord_dto import NewsRecord_dto
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestWebsiteFacade(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Reset singleton before tests
        WebsiteFacade.reset_instance()
    
    def setUp(self):
        # Reset singleton before each test
        WebsiteFacade.reset_instance()
        self.facade = WebsiteFacade()
        
        # Mock DAL controller
        self.mock_dal = Mock()
        self.facade.dal_controller = self.mock_dal
        
        # Mock website repository
        self.mock_website_repo = Mock()
        self.mock_dal.website_repo = self.mock_website_repo
        
        # Mock publications repository
        self.mock_pubs_repo = Mock()
        self.mock_dal.publications_repo = self.mock_pubs_repo
        
        # Mock news repository
        self.mock_news_repo = Mock()
        self.mock_dal.News_repo = self.mock_news_repo
    
    def tearDown(self):
        # Reset singleton after each test
        WebsiteFacade.reset_instance()
    
    def test_singleton_pattern(self):
        facade1 = WebsiteFacade()
        facade2 = WebsiteFacade()
        self.assertIs(facade1, facade2)
    
    def test_get_instance(self):
        facade1 = WebsiteFacade.get_instance()
        facade2 = WebsiteFacade.get_instance()
        self.assertIs(facade1, facade2)
    
    def test_reset_instance(self):
        facade1 = WebsiteFacade()
        WebsiteFacade.reset_instance()
        facade2 = WebsiteFacade()
        self.assertIsNot(facade1, facade2)
    
    def test_initialization(self):
        self.assertIsNotNone(self.facade.websites)
        self.assertIsNotNone(self.facade.dal_controller)
        self.assertTrue(self.facade._initialized)
    
    def test_add_website(self):
        website = Website("test.com")
        self.facade.add_website(website)
        self.assertIn("test.com", self.facade.websites)
        self.assertEqual(self.facade.websites["test.com"], website)
    
    def test_create_new_website(self):
        domain = "newlab.com"
        self.facade.create_new_website(domain)
        
        self.assertIn(domain, self.facade.websites)
        website = self.facade.websites[domain]
        self.assertEqual(website.domain, domain)
        self.mock_website_repo.save.assert_called_once()
    
    def test_get_website_existing(self):
        website = Website("test.com")
        self.facade.websites["test.com"] = website
        
        result = self.facade.get_website("test.com")
        self.assertEqual(result, website)

    def test_get_website_not_existing_not_loaded(self):
        self.mock_website_repo.find_by_domain.return_value = None
        
        with self.assertRaises(Exception) as context:
            self.facade.get_website("nonexistent.com")
        
        self.assertEqual(str(context.exception), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)
    
    def test_get_all_website_domains(self):
        expected_domains = ["lab1.com", "lab2.com", "lab3.com"]
        self.mock_website_repo.find_all_domains.return_value = expected_domains
        
        result = self.facade.get_all_website_domains()
        
        self.mock_website_repo.find_all_domains.assert_called_once()
        self.assertEqual(result, expected_domains)
    
    def test_get_all_approved_publication(self):
        website = Mock()
        expected_pubs = [PublicationDTO("Test Pub", 2023, "http://test.com", ["Author"])]
        website.get_all_approved_publication.return_value = expected_pubs
        self.facade.websites["test.com"] = website
        
        result = self.facade.get_all_approved_publication("test.com")
        
        website.get_all_approved_publication.assert_called_once()
        self.assertEqual(result, expected_pubs)
    
    def test_get_all_not_approved_publications(self):
        website = Mock()
        expected_pubs = [PublicationDTO("Test Pub", 2023, "http://test.com", ["Author"])]
        website.get_all_not_approved_publications.return_value = expected_pubs
        self.facade.websites["test.com"] = website
        
        result = self.facade.get_all_not_approved_publications("test.com")
        
        website.get_all_not_approved_publications.assert_called_once()
        self.assertEqual(result, expected_pubs)
    
    def test_create_new_publication(self):
        website = Mock()
        mock_pub_dto = Mock()
        mock_pub_dto.get_paper_id.return_value = "pub123"
        website.add_publication_manually.return_value = mock_pub_dto
        self.facade.websites["test.com"] = website
        
        result = self.facade.create_new_publication(
            "test.com", "http://pub.com", "Test Publication", 
            "http://git.com", "http://video.com", "http://presentation.com", 
            ["author@test.com"]
        )
        
        website.add_publication_manually.assert_called_once_with(
            "http://pub.com", "Test Publication", "http://git.com", 
            "http://video.com", "http://presentation.com", ["author@test.com"]
        )
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=mock_pub_dto, domain="test.com")
        self.assertEqual(result, "pub123")
    
    def test_create_new_publication_fromDTO(self):
        website = Mock()
        pub_dto = PublicationDTO("Test Pub", 2023, "http://test.com", ["Author"])
        self.facade.websites["test.com"] = website
        
        self.facade.create_new_publication_fromDTO("test.com", pub_dto, ["author@test.com"])
        
        website.create_publication.assert_called_once_with(publicationDTO=pub_dto, authors_emails=["author@test.com"])
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=pub_dto, domain="test.com")
    
    def test_update_publication(self):
        website = Mock()
        pub_dto = PublicationDTO("Test Pub", 2023, "http://test.com", ["Author"])
        self.facade.websites["test.com"] = website
        
        self.facade.update_publication("test.com", pub_dto)
        
        website.update_publication.assert_called_once_with(pub_dto)
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=pub_dto, domain="test.com")
    
    def test_set_publication_video_link(self):
        website = Mock()
        mock_pub_dto = Mock()
        website.set_publication_video_link.return_value = mock_pub_dto
        self.facade.websites["test.com"] = website
        
        self.facade.set_publication_video_link("test.com", "pub123", "http://video.com")
        
        website.set_publication_video_link.assert_called_once_with("pub123", "http://video.com")
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=mock_pub_dto, domain="test.com")
    
    def test_set_publication_git_link(self):
        website = Mock()
        mock_pub_dto = Mock()
        website.set_publication_git_link.return_value = mock_pub_dto
        self.facade.websites["test.com"] = website
        
        self.facade.set_publication_git_link("test.com", "pub123", "http://git.com")
        
        website.set_publication_git_link.assert_called_once_with("pub123", "http://git.com")
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=mock_pub_dto, domain="test.com")
    
    def test_set_publication_presentation_link(self):
        website = Mock()
        mock_pub_dto = Mock()
        website.set_publication_presentation_link.return_value = mock_pub_dto
        self.facade.websites["test.com"] = website
        
        self.facade.set_publication_presentation_link("test.com", "pub123", "http://presentation.com")
        
        website.set_publication_presentation_link.assert_called_once_with("pub123", "http://presentation.com")
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=mock_pub_dto, domain="test.com")
    
    def test_error_if_member_is_not_publication_author(self):
        website = Mock()
        website.check_if_member_is_publication_author.return_value = False
        self.facade.websites["test.com"] = website
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_member_is_not_publication_author("test.com", "pub123", "user@test.com")
        
        self.assertEqual(str(context.exception), ExceptionsEnum.USER_IS_NOT_PUBLICATION_AUTHOR_OR_LAB_MANAGER.value)
    
    def test_error_if_publication_is_rejected(self):
        website = Mock()
        website.is_publication_rejected.return_value = True
        self.facade.websites["test.com"] = website
        
        with self.assertRaises(Exception) as context:
            self.facade.error_if_publication_is_rejected("test.com", "pub123")
        
        self.assertEqual(str(context.exception), ExceptionsEnum.PUBLICATION_ALREADY_REJECTED.value)
    
    def test_check_if_publication_approved(self):
        website = Mock()
        website.check_if_publication_approved.return_value = True
        self.facade.websites["test.com"] = website
        
        result = self.facade.check_if_publication_approved("test.com", "pub123")
        
        website.check_if_publication_approved.assert_called_once_with("pub123")
        self.assertTrue(result)
    
    def test_get_publication_by_paper_id(self):
        website = Mock()
        expected_pub = PublicationDTO("Test Pub", 2023, "http://test.com", ["Author"])
        website.get_publication_by_paper_id.return_value = expected_pub
        self.facade.websites["test.com"] = website
        
        result = self.facade.get_publication_by_paper_id("test.com", "pub123")
        
        website.get_publication_by_paper_id.assert_called_once_with("pub123")
        self.assertEqual(result, expected_pub)
    
    def test_final_approve_publication(self):
        website = Mock()
        mock_pub_dto = Mock()
        website.final_approve_publication.return_value = mock_pub_dto
        self.facade.websites["test.com"] = website
        
        self.facade.final_approve_publication("test.com", "pub123")
        
        website.final_approve_publication.assert_called_once_with("pub123")
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=mock_pub_dto, domain="test.com")
    
    def test_set_site_about_us(self):
        website = Mock()
        self.facade.websites["test.com"] = website
        
        self.facade.set_site_about_us("test.com", "About our lab")
        
        website.set_about_us.assert_called_once_with("About our lab")
        self.mock_website_repo.save.assert_called_once()
    
    def test_set_site_contact_info(self):
        website = Mock()
        contact_info_dto = Mock()
        self.facade.websites["test.com"] = website
        
        self.facade.set_site_contact_info("test.com", contact_info_dto)
        
        website.set_contact_info.assert_called_once_with(contact_info_dto)
        self.mock_website_repo.save.assert_called_once()
    
    def test_get_about_us(self):
        website = Mock()
        website.get_about_us.return_value = "About our lab"
        self.facade.websites["test.com"] = website
        
        result = self.facade.get_about_us("test.com")
        
        website.get_about_us.assert_called_once()
        self.assertEqual(result, "About our lab")
    
    def test_initial_approve_publication(self):
        website = Mock()
        mock_pub_dto = Mock()
        website.initial_approve_publication.return_value = mock_pub_dto
        self.facade.websites["test.com"] = website
        
        self.facade.initial_approve_publication("test.com", "pub123")
        
        website.initial_approve_publication.assert_called_once_with("pub123")
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=mock_pub_dto, domain="test.com")
    
    def test_reject_publication(self):
        website = Mock()
        mock_pub_dto = Mock()
        website.reject_publication.return_value = mock_pub_dto
        self.facade.websites["test.com"] = website
        
        self.facade.reject_publication("test.com", "pub123")
        
        website.reject_publication.assert_called_once_with("pub123")
        self.mock_pubs_repo.save.assert_called_once_with(publication_dto=mock_pub_dto, domain="test.com")
    
    def test_get_contact_us(self):
        website = Mock()
        website.get_contact_us.return_value = ContactInfo("Test Address", "test@lab.com", "123-456-7890")
        self.facade.websites["test.com"] = website
        
        result = self.facade.get_contact_us("test.com")
        
        website.get_contact_us.assert_called_once()
        self.assertIsInstance(result, ContactInfo)
    
    def test_add_news_record(self):
        website = Mock()
        self.facade.websites["test.com"] = website
        
        self.facade.add_news_record("test.com", "New research published", "http://news.com", "2023-12-01")
        
        website.add_news_record.assert_called_once()
        self.mock_news_repo.save_news_record.assert_called_once()
        
        # Verify the news record DTO was created correctly
        call_args = self.mock_news_repo.save_news_record.call_args[1]['news_record_dto']
        self.assertEqual(call_args.domain, "test.com")
        self.assertEqual(call_args.text, "New research published")
        self.assertEqual(call_args.link, "http://news.com")
        # Accept both string and datetime for date
        if hasattr(call_args.date, 'strftime'):
            self.assertEqual(call_args.date.strftime("%Y-%m-%d"), "2023-12-01")
        else:
            self.assertEqual(call_args.date, "2023-12-01")
    
    def test_get_news(self):
        website = Mock()
        expected_dict = {"id": "1", "domain": "test.com", "text": "News 1", "link": "http://1.com", "date": "2023-12-01"}
        news_obj = Mock()
        news_obj.get_json.return_value = expected_dict
        website.get_news.return_value = [news_obj]
        self.facade.websites["test.com"] = website
        
        result = self.facade.get_news("test.com")
        
        website.get_news.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], expected_dict)

if __name__ == '__main__':
    unittest.main() 