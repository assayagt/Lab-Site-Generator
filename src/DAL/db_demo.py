import unittest
import uuid

from database_manager import DatabaseManager
from DAL_controller import DAL_controller
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from DTOs.Website_dto import website_dto
from DTOs.Notification_dto import notification_dto
from DTOs.SiteCustom_dto import siteCustom_dto
from DTOs.LabMember_dto import lab_member_dto

class TestPublicationRepository(unittest.TestCase):
    def setUp(self):
        # Use in-memory SQLite DB for test isolation
        self.db_manager = DatabaseManager(db_path=":memory:")
        DAL_controller.reset_instance()
        self.controller = DAL_controller(db_manager=self.db_manager)

        self.pub_repo = self.controller.publications_repo
        self.members_repo = self.controller.members_repo
        self.websites_repo = self.controller.website_repo

        self.test_domain = "test-domain"
        self.test_email = "user@example.com"
        self.test_email2 = "user2@example.com"

        self.website_dto = website_dto(
                domain=self.test_domain,
                contact_info="Some contact info",
                about_us="About section"
            )
        

        # Seed required data
        self.members_repo.save_member(self.test_email)
        self.websites_repo.save(
            website_dto=self.website_dto,
            user_email=self.test_email
        )

    def test_find_websites_by_email(self):
        second_web_dto = website_dto(
            domain="self.test_domain",
            contact_info="Some contact info",
            about_us="About section"
        )
        self.websites_repo.save(
            website_dto=second_web_dto,
            user_email=self.test_email
        )
        result = self.controller.website_repo.find_by_email(self.test_email)
        self.assertIsNotNone(result)
        self.assertEqual(2, len(result))

    def test_insert_and_find_notification(self):
        _id = str(uuid.uuid4())
        _notification_dto = notification_dto(
            domain=self.test_domain,
            id=_id,
            body="Register me",
            recipient=self.test_email,
            subject="regregreg",
            request_email=self.test_email2,
            isRead= False
        )
        self.assertTrue(self.controller.notifications_repo.save_notification(_notification_dto))
        retrieved = self.controller.notifications_repo.find_notifications_by_domain_email(self.test_domain, self.test_email)
        self.assertIsNotNone(retrieved)

    def test_insert_and_find_siteCustom(self):
        _siteCustomDTO = siteCustom_dto(
            domain=self.test_domain,
            name="some name",
            components_str="comp1, comp2, comp3",
            template="template1",
            site_creator_email=self.test_email,
            logo="some path to a logo",
            home_picture="some path to homePic",
            generated=False
        )
        self.assertTrue(self.controller.siteCustom_repo.save(_siteCustomDTO))
        retrieved = self.controller.siteCustom_repo.find_by_domain(self.test_domain)
        self.assertIsNotNone(retrieved)
        retrieved = self.controller.siteCustom_repo.find_by_email(self.test_email)
        self.assertIsNotNone(retrieved)

    def test_insert_and_find_labMember(self):
        _labMember_dto = lab_member_dto(
            domain=self.test_domain,
            email=self.test_email,
            second_email=self.test_email2,
            linkedin_link="linkedin",
            full_name="website creator",
            degree = "PHD"
        )
        self.assertTrue(self.controller.LabMembers_repo.save_LabMember(_labMember_dto))
        result = self.controller.LabMembers_repo.find_LabMember_by_domain_email(self.test_domain, self.test_email)
        self.assertIsNotNone(result)


    def test_insert_and_find_publication(self):
        pub_id = str(uuid.uuid4())
        pub = PublicationDTO(
            paper_id=pub_id,
            title="Test Publication",
            authors="Alice, Bob",
            publication_year=2024,
            approved="Yes",
            publication_link="https://pub.link",
            git_link="https://github.com/example",
            video_link=None,
            presentation_link=None,
            description="A study about testing"
        )
        success = self.pub_repo.save(pub, self.test_domain)
        self.assertTrue(success)

        retrieved = self.pub_repo.find_by_id(pub_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, pub.title)

    def test_update_publication(self):
        pub_id = str(uuid.uuid4())
        pub = PublicationDTO(
            paper_id=pub_id,
            title="Initial Title",
            authors="John Smith",
            publication_year=2023,
            approved="No",
            publication_link="http://init.link",
            git_link="",
            video_link="",
            presentation_link="",
            description="Initial description"
        )
        self.pub_repo.save(pub, self.test_domain)

        pub.title = "Updated Title"
        self.pub_repo.save(pub, self.test_domain)

        updated = self.pub_repo.find_by_id(pub_id)
        self.assertEqual(updated.title, "Updated Title")

    def test_delete_publication(self):
        pub_id = str(uuid.uuid4())
        pub = PublicationDTO(
            paper_id=pub_id,
            title="To Be Deleted",
            authors="Anonymous",
            publication_year=2022,
            approved="Yes",
            publication_link="http://delete.me",
            git_link="",
            video_link="",
            presentation_link="",
            description="Test delete operation"
        )
        self.pub_repo.save(pub, self.test_domain)

        deleted = self.pub_repo.delete(pub_id)
        self.assertTrue(deleted)

        missing = self.pub_repo.find_by_id(pub_id)
        self.assertIsNone(missing)


if __name__ == "__main__":
    unittest.main()
