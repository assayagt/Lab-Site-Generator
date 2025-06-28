import unittest
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus

class TestPublicationDTO(unittest.TestCase):
    def setUp(self):
        self.publication = PublicationDTO(
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

    def test_to_dict(self):
        pub_dict = self.publication.to_dict()
        self.assertEqual(pub_dict['title'], 'Test Publication')
        self.assertEqual(pub_dict['publication_year'], 2023)
        self.assertEqual(pub_dict['authors'], ['Author 1', 'Author 2'])
        self.assertEqual(pub_dict['status'], ApprovalStatus.INITIAL_PENDING.value)
        self.assertEqual(pub_dict['domain'], 'lab.example.com')
        self.assertIn('paper_id', pub_dict)

    def test_equality_same_title_and_year(self):
        pub1 = PublicationDTO(
            title='Same Title',
            publication_year=2023,
            publication_link='http://example1.com'
        )
        pub2 = PublicationDTO(
            title='Same Title',
            publication_year=2023,
            publication_link='http://example2.com'
        )
        self.assertEqual(pub1, pub2)

    def test_equality_different_title(self):
        pub1 = PublicationDTO(
            title='Title 1',
            publication_year=2023,
            publication_link='http://example.com'
        )
        pub2 = PublicationDTO(
            title='Title 2',
            publication_year=2023,
            publication_link='http://example.com'
        )
        self.assertNotEqual(pub1, pub2)

    def test_equality_different_year(self):
        pub1 = PublicationDTO(
            title='Same Title',
            publication_year=2023,
            publication_link='http://example.com'
        )
        pub2 = PublicationDTO(
            title='Same Title',
            publication_year=2024,
            publication_link='http://example.com'
        )
        self.assertNotEqual(pub1, pub2)

    def test_equality_case_insensitive_title(self):
        pub1 = PublicationDTO(
            title='Test Title',
            publication_year=2023,
            publication_link='http://example.com'
        )
        pub2 = PublicationDTO(
            title='test title',
            publication_year=2023,
            publication_link='http://example.com'
        )
        self.assertEqual(pub1, pub2)

    def test_hash_consistency(self):
        pub1 = PublicationDTO(
            title='Test Title',
            publication_year=2023,
            publication_link='http://example.com'
        )
        pub2 = PublicationDTO(
            title='Test Title',
            publication_year=2023,
            publication_link='http://example.com'
        )
        self.assertEqual(hash(pub1), hash(pub2))

    def test_set_video_link(self):
        self.publication.set_video_link('http://newvideo.com')
        self.assertEqual(self.publication.video_link, 'http://newvideo.com')

    def test_set_git_link(self):
        self.publication.set_git_link('http://newgit.com')
        self.assertEqual(self.publication.git_link, 'http://newgit.com')

    def test_set_presentation_link(self):
        self.publication.set_presentation_link('http://newslides.com')
        self.assertEqual(self.publication.presentation_link, 'http://newslides.com')

    def test_set_description(self):
        self.publication.set_description('New description')
        self.assertEqual(self.publication.description, 'New description')

    def test_set_authors(self):
        new_authors = ['New Author 1', 'New Author 2']
        self.publication.set_authors(new_authors)
        self.assertEqual(self.publication.authors, new_authors)

    def test_set_author_emails(self):
        new_emails = ['newauthor1@example.com', 'newauthor2@example.com']
        self.publication.set_author_emails(new_emails)
        self.assertEqual(self.publication.author_emails, new_emails)

    def test_set_domain(self):
        self.publication.set_domain('newlab.example.com')
        self.assertEqual(self.publication.domain, 'newlab.example.com')

    def test_get_paper_id(self):
        paper_id = self.publication.get_paper_id()
        self.assertIsNotNone(paper_id)
        self.assertIsInstance(paper_id, str)

    def test_get_authors(self):
        authors = self.publication.get_authors()
        self.assertEqual(authors, ['Author 1', 'Author 2'])

    def test_get_description(self):
        description = self.publication.get_description()
        self.assertEqual(description, 'Test description')

    def test_get_domain(self):
        domain = self.publication.get_domain()
        self.assertEqual(domain, 'lab.example.com')

if __name__ == '__main__':
    unittest.main() 