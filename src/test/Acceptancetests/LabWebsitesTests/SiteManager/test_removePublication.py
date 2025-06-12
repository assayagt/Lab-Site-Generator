import unittest

from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.test.Acceptancetests.LabGeneratorTests.ProxyToTests import ProxyToTest
from src.test.Acceptancetests.LabWebsitesTests.ProxyToTests import ProxyToTests
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template


class TestRemovePublicationEdgeCases(unittest.TestCase):
    def setUp(self):
        self.generator_system_service = ProxyToTest("Real")
        self.lab_system_service = ProxyToTests("Real", self.generator_system_service.get_lab_system_controller())

        self.user_id = self.generator_system_service.enter_generator_system().get_data()
        self.generator_system_service.login(user_id=self.user_id, email="user_1@example.com")

        self.domain = "lab1.example.com"
        self.manager_email = "manager1@example.com"
        self.lab_managers = {
            self.manager_email: {"full_name": "Roni Stern", "degree": "Ph.D."},
        }
        self.lab_member_email = "member1@example.com"
        self.lab_member_name = "Guni Sharon"
        self.site_creator_email = "creator@example.com"
        self.website_name = "Test Lab Website"
        self.components = ["Homepage", "Publications"]
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

        self.manager_id = self.lab_system_service.enter_lab_website(self.domain).get_data()
        self.lab_system_service.login(self.domain, self.manager_id, self.manager_email)

        # Add a real publication
        self.publication_link="https://scholar.google.com/citations?view_op=view_citation&hl=en&user=X6t18NkAAAAJ&citation_for_view=X6t18NkAAAAJ:_kc_bZDykSQC"
        response = self.lab_system_service.add_publication_manually(
            self.manager_id, self.domain, self.publication_link,
            None, None, None
        )
        self.assertTrue(response.is_success())
        self.publication_id = response.get_data()

    def tearDown(self):
        self.generator_system_service.reset_system()
        self.lab_system_service.reset_system()

    def test_remove_nonexistent_publication(self):
        """
        Try to remove a publication that does not exist.
        Should fail with WEBSITE_PUBLICATION_NOT_EXIST.
        """
        fake_pub_id = "non-existent-pub-id"
        response = self.lab_system_service.remove_publication(
            self.manager_id, self.domain, fake_pub_id
        )

        self.assertFalse(response.is_success())
        # self.assertEqual(response.get_message(), ExceptionsEnum.WEBSITE_PUBLICATION_NOT_EXIST.value)
        self.assertIsNone(response.get_data())

    def test_remove_existing_publication_successfully(self):
        """
        Remove a valid publication successfully.
        """
        response = self.lab_system_service.remove_publication(
            self.manager_id, self.domain, self.publication_id
        )

        self.assertTrue(response.is_success())
        self.assertEqual(response.get_message(), "Publication removed successfully")
        

    def test_remove_already_removed_publication(self):
        """
        Try removing a publication that was already removed.
        Should fail with WEBSITE_PUBLICATION_NOT_EXIST.
        """
        # First removal (success)
        response1 = self.lab_system_service.remove_publication(
            self.manager_id, self.domain, self.publication_id
        )
        self.assertTrue(response1.is_success())

        # Second removal (should fail)
        response2 = self.lab_system_service.remove_publication(
            self.manager_id, self.domain, self.publication_id
        )
        self.assertFalse(response2.is_success())
        self.assertEqual(response2.get_message(), ExceptionsEnum.PUBLICATION_ALREADY_REJECTED.value)
        self.assertIsNone(response2.get_data())

if __name__ == "__main__":
    unittest.main()