import unittest
from unittest.mock import patch, MagicMock
from src.main.DomainLayer.LabWebsites.Website.Website import Website
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.ContactInfo import ContactInfo
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestWebsite(unittest.TestCase):
    def setUp(self):
        self.website = Website(domain='lab.example.com')
        self.contact_info = ContactInfo('123 Main St', 'lab@example.com', '123-456-7890')
        self.website.contact_info = self.contact_info
        self.website.about_us = 'About our lab'

    def test_create_publication(self):
        publication = PublicationDTO(
            title='Test Publication',
            publication_year=2023,
            publication_link='http://example.com',
            approved=ApprovalStatus.INITIAL_PENDING,
            git_link='http://github.com',
            authors=['Author 1', 'Author 2'],
            video_link='http://youtube.com',
            presentation_link='http://slides.com',
            description='Test description',
            author_emails=['author1@example.com', 'author2@example.com'],
            domain='lab.example.com'
        )
        self.website.create_publication(publication, ['author1@example.com', 'author2@example.com'])
        self.assertIn('author1@example.com', self.website.members_publications)
        self.assertIn('author2@example.com', self.website.members_publications)
        self.assertIn(publication, self.website.members_publications['author1@example.com'])

    def test_create_duplicate_publication_raises_exception(self):
        publication = PublicationDTO(
            title='Test Publication',
            publication_year=2023,
            publication_link='http://example.com',
            approved=ApprovalStatus.APPROVED,
            git_link='http://github.com',
            authors=['Author 1'],
            video_link='http://youtube.com',
            presentation_link='http://slides.com',
            description='Test description',
            author_emails=['author1@example.com'],
            domain='lab.example.com'
        )
        self.website.create_publication(publication, ['author1@example.com'])
        with self.assertRaises(Exception) as context:
            self.website.create_publication(publication, ['author1@example.com'])
        self.assertEqual(str(context.exception), ExceptionsEnum.PUBLICATION_ALREADY_APPROVED.value)

    def test_check_publication_exist(self):
        publication = PublicationDTO(
            title='Test Publication',
            publication_year=2023,
            publication_link='http://example.com',
            approved=ApprovalStatus.INITIAL_PENDING,
            git_link='http://github.com',
            authors=['Author 1'],
            video_link='http://youtube.com',
            presentation_link='http://slides.com',
            description='Test description',
            author_emails=['author1@example.com'],
            domain='lab.example.com'
        )
        self.website.create_publication(publication, ['author1@example.com'])
        self.assertTrue(self.website.check_publication_exist(publication))

    def test_get_all_approved_publications(self):
        publication1 = PublicationDTO(
            title='Test Publication 1',
            publication_year=2023,
            publication_link='http://example1.com',
            approved=ApprovalStatus.APPROVED,
            git_link='http://github1.com',
            authors=['Author 1'],
            video_link='http://youtube1.com',
            presentation_link='http://slides1.com',
            description='Test description 1',
            author_emails=['author1@example.com'],
            domain='lab.example.com'
        )
        publication2 = PublicationDTO(
            title='Test Publication 2',
            publication_year=2023,
            publication_link='http://example2.com',
            approved=ApprovalStatus.INITIAL_PENDING,
            git_link='http://github2.com',
            authors=['Author 2'],
            video_link='http://youtube2.com',
            presentation_link='http://slides2.com',
            description='Test description 2',
            author_emails=['author2@example.com'],
            domain='lab.example.com'
        )
        self.website.create_publication(publication1, ['author1@example.com'])
        self.website.create_publication(publication2, ['author2@example.com'])
        approved_publications = self.website.get_all_approved_publication()
        self.assertEqual(len(approved_publications), 1)
        self.assertEqual(approved_publications[0]['title'], 'Test Publication 1')

    def test_final_approve_publication(self):
        publication = PublicationDTO(
            title='Test Publication',
            publication_year=2023,
            publication_link='http://example.com',
            approved=ApprovalStatus.INITIAL_PENDING,
            git_link='http://github.com',
            authors=['Author 1'],
            video_link='http://youtube.com',
            presentation_link='http://slides.com',
            description='Test description',
            author_emails=['author1@example.com'],
            domain='lab.example.com'
        )
        self.website.create_publication(publication, ['author1@example.com'])
        approved_publication = self.website.final_approve_publication(publication.get_paper_id())
        self.assertEqual(approved_publication.approved, ApprovalStatus.APPROVED)

    def test_reject_publication(self):
        publication = PublicationDTO(
            title='Test Publication',
            publication_year=2023,
            publication_link='http://example.com',
            approved=ApprovalStatus.INITIAL_PENDING,
            git_link='http://github.com',
            authors=['Author 1'],
            video_link='http://youtube.com',
            presentation_link='http://slides.com',
            description='Test description',
            author_emails=['author1@example.com'],
            domain='lab.example.com'
        )
        self.website.create_publication(publication, ['author1@example.com'])
        rejected_publication = self.website.reject_publication(publication.get_paper_id())
        self.assertEqual(rejected_publication.approved, ApprovalStatus.REJECTED)

    def test_set_about_us(self):
        self.website.set_about_us('New about us text')
        self.assertEqual(self.website.get_about_us(), 'New about us text')

    def test_set_contact_info(self):
        new_contact_info = ContactInfo('456 Oak St', 'newlab@example.com', '987-654-3210')
        self.website.set_contact_info(new_contact_info)
        contact_dict = self.website.get_contact_us()
        self.assertEqual(contact_dict['address'], '456 Oak St')
        self.assertEqual(contact_dict['email'], 'newlab@example.com')
        self.assertEqual(contact_dict['phone_num'], '987-654-3210')

if __name__ == '__main__':
    unittest.main() 