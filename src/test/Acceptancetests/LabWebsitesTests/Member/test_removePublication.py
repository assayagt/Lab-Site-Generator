import unittest

from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.Util.Response import Response


class TestRemovePub(unittest.TestCase):
    def setUp(self):
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        self.domain = "lab1.example.com"
        self.site_creator_email = "creator@example.com"
        self.lab_member_email = "member1@example.com"
        self.lab_member_name = "Guni Sharon"
        self.lab_managers = {
            "manager1@example.com": {"full_name": "Roni Stern", "degree": "Ph.D."},
        }
        self.website_name = "Lab Website"
        self.components = ["Homepage", "Contact Us", "Research"]
        self.template = Template.template1

        self.generator_system_service.create_website(
            self.user_id, self.website_name, self.domain, self.components, self.template
        )

        self.generator_system_service.create_new_lab_website(
            self.domain,
            {self.lab_member_email: {"full_name": self.lab_member_name, "degree": "Ph.D."}},
            self.lab_managers,
            {"email": self.site_creator_email, "full_name": "Site Creator", "degree": "Ph.D."},
            ""
        )

        self.member_id = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.member_id, self.lab_member_email)

        self.manager_id = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.manager_id, "manager1@example.com")

        
        publication_link="https://scholar.google.com/citations?view_op=view_citation&hl=en&user=X6t18NkAAAAJ&citation_for_view=X6t18NkAAAAJ:_kc_bZDykSQC"
        # Perform the operation
        add_response = self.lab_system_service.add_publication_manually(
            self.manager_id, self.domain, publication_link,
            None, None, None  # Pass None for git_link, video_link, and presentation_link if not provided
        )
        self.assertTrue(add_response.is_success())
        self.publication_id = add_response.get_data()

    def tearDown(self):
        self.generator_system_service.reset_system()
        self.lab_system_service.reset_system()

    def test_remove_publication_by_non_manager_fails(self):
        """
        A regular lab member should not be able to remove a publication.
        """
        response = self.lab_system_service.remove_publication(
            self.member_id, self.domain, self.publication_id
        )
        print(response)
        self.assertFalse(response.is_success())
        self.assertIsNone(response.get_data())
        self.assertEqual(response.get_message(), ExceptionsEnum.USER_IS_NOT_A_LAB_MANAGER_OR_CREATOR.value)

if __name__ == "__main__":
    unittest.main()
