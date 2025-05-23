import unittest
import uuid

from src.DAL.database_manager import DatabaseManager
from src.DAL.DAL_controller import DAL_controller
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.DAL.DTOs.Website_dto import website_dto
from src.DAL.DTOs.Notification_dto import notification_dto
from src.DAL.DTOs.SiteCustom_dto import siteCustom_dto
from src.DAL.DTOs.LabMember_dto import lab_member_dto

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

        self.site_custom_dto = siteCustom_dto(
            domain=self.test_domain,
            name="some name",
            components_str="comp1, comp2, comp3",
            template="template1",
            site_creator_email=self.test_email,
            logo="some path to a logo",
            home_picture="some path to homePic",
            generated=False
        )
        self.website_dto = website_dto(
            domain=self.test_domain,
            contact_info="golden pages",
            about_us="LSG LSG"
        )

        # Seed required data a user with a site custom and a deployed website
        self.members_repo.save_member(self.test_email)
        self.controller.siteCustom_repo.save(self.site_custom_dto, self.test_email)
        self.websites_repo.save(self.website_dto)

    def test_find_websites(self):
        result = self.controller.website_repo.find_by_domain(self.test_domain)
        self.assertIsNotNone(result)


    def test_siteCustom_creation(self):
        creatorEmail = "creator@example.com"
        ex_domain = "example_comain.52.82"
        self.controller.members_repo.save_member(creatorEmail)
        _site_custom_dto = siteCustom_dto(
            domain=ex_domain,
            name="some name",
            components_str="comp1, comp2, comp3",
            template="template1",
            site_creator_email=creatorEmail,
            logo="some path to a logo",
            home_picture="some path to homePic",
            generated=False
        )
        self.assertTrue(self.controller.siteCustom_repo.save(_site_custom_dto, creatorEmail))
        _site_custom_dto.components_str = "comp1, comp2"
        self.assertTrue(self.controller.siteCustom_repo.save(_site_custom_dto))
        


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

    def test_update_and_find_siteCustom(self):
        _siteCustomDTO = siteCustom_dto(
            domain=self.test_domain,
            name="some name updated",
            components_str="comp1, comp2, comp3",
            template="template1",
            site_creator_email=self.test_email,
            logo="some path to a logo",
            home_picture="some path to homePic",
            generated=False
        )
        self.assertTrue(self.controller.siteCustom_repo.save(_siteCustomDTO, self.test_email))
        retrieved = self.controller.siteCustom_repo.find_by_domain(self.test_domain)
        self.assertIsNotNone(retrieved)
        retrieved_lst = self.controller.siteCustom_repo.find_by_email(self.test_email)
        self.assertIsNotNone(retrieved_lst)
        self.assertEqual(_siteCustomDTO.name, retrieved.name)

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
            description="A study about testing",
            author_emails=["ani@gmail.com", "ata@jamal.com"]
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
            description="Initial description",
            author_emails=["ani@gmail.com", "ata@jamal.com"]
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
            description="Test delete operation",
            author_emails=["ani@gmail.com", "ata@jamal.com"]
        )
        self.pub_repo.save(pub, self.test_domain)

        deleted = self.pub_repo.delete(pub_id)
        self.assertTrue(deleted)

        missing = self.pub_repo.find_by_id(pub_id)
        self.assertIsNone(missing)


if __name__ == "__main__":
    unittest.main()
