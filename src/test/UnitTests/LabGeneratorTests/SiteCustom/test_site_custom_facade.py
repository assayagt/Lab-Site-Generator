import unittest
from unittest.mock import Mock, patch

from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustomFacade import SiteCustomFacade
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabGenerator.User.User import User
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestSiteCustomFacade(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.site_custom_facade = SiteCustomFacade()
        self.test_user = User("test_user")
        self.test_email = "test@example.com"
        self.test_template = Template.template1
        self.test_components = ["About", "Contact", "Publications"]
        self.test_domain = "test-lab.com"
        self.test_site = SiteCustom(
            domain=self.test_domain,
            name="Test Lab",
            components=self.test_components,
            template=self.test_template,
            site_creator_email=self.test_email,
            logo=None,
            home_picture=None,
            generated=False,
            gallery_path=None
        )

    def test_create_new_site(self):
        """Test creating a new site."""
        with patch.object(self.site_custom_facade, 'error_if_domain_is_not_valid') as mock_validate:
            mock_validate.return_value = None
            result = self.site_custom_facade.create_new_site(
                domain=self.test_domain,
                name="New Lab",
                components=self.test_components,
                template=self.test_template,
                email=self.test_email
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, SiteCustom)
            self.assertEqual(result.domain, self.test_domain)
            self.assertEqual(result.name, "New Lab")
            self.assertEqual(result.components, self.test_components)
            self.assertEqual(result.template, self.test_template)
            self.assertEqual(result.site_creator_email, self.test_email)

    def test_change_site_name(self):
        """Test changing site name."""
        with patch.object(self.site_custom_facade, 'sites', {self.test_domain: self.test_site}):
            new_name = "Updated Lab"
            self.site_custom_facade.change_site_name(self.test_domain, new_name)
            self.assertEqual(self.site_custom_facade.sites[self.test_domain].name, new_name)

    def test_change_site_domain(self):
        """Test changing site domain."""
        with patch.object(self.site_custom_facade, 'sites', {self.test_domain: self.test_site}):
            new_domain = "updated-lab.com"
            self.site_custom_facade.change_site_domain(self.test_domain, new_domain)
            self.assertIn(new_domain, self.site_custom_facade.sites)
            self.assertNotIn(self.test_domain, self.site_custom_facade.sites)

    def test_change_site_template(self):
        """Test changing site template."""
        with patch.object(self.site_custom_facade, 'sites', {self.test_domain: self.test_site}):
            new_template = Template.template2
            self.site_custom_facade.change_site_template(self.test_domain, new_template)
            self.assertEqual(self.site_custom_facade.sites[self.test_domain].template, new_template)

    def test_add_components_to_site(self):
        """Test adding components to site."""
        with patch.object(self.site_custom_facade, 'sites', {self.test_domain: self.test_site}):
            new_components = ["Media", "News"]
            self.site_custom_facade.add_components_to_site(self.test_domain, new_components)
            self.assertEqual(self.site_custom_facade.sites[self.test_domain].components, new_components)

    def test_remove_component_from_site(self):
        """Test removing component from site."""
        with patch.object(self.site_custom_facade, 'sites', {self.test_domain: self.test_site}):
            self.site_custom_facade.remove_component_from_site(self.test_domain, "About")
            self.assertNotIn("About", self.site_custom_facade.sites[self.test_domain].components)

    def test_set_custom_site_as_generated(self):
        """Test setting site as generated."""
        with patch.object(self.site_custom_facade, 'sites', {self.test_domain: self.test_site}):
            self.site_custom_facade.set_custom_site_as_generated(self.test_domain)
            self.assertTrue(self.site_custom_facade.sites[self.test_domain].generated)

    def test_set_logo_and_home_picture(self):
        """Test setting logo and home picture."""
        with patch.object(self.site_custom_facade, 'sites', {self.test_domain: self.test_site}):
            logo = "logo.png"
            home_picture = "home.jpg"
            self.site_custom_facade.set_logo(self.test_domain, logo)
            self.site_custom_facade.set_home_picture(self.test_domain, home_picture)
            self.assertEqual(self.site_custom_facade.sites[self.test_domain].logo, logo)
            self.assertEqual(self.site_custom_facade.sites[self.test_domain].home_picture, home_picture)

    def test_error_handling(self):
        """Test error handling in facade methods."""
        with patch.object(self.site_custom_facade, 'sites', {}):
            # Test domain not exist
            with self.assertRaises(Exception) as context:
                self.site_custom_facade.change_site_name("nonexistent.com", "New Name")
            self.assertEqual(str(context.exception), ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

            # Test invalid site name
            with self.assertRaises(Exception) as context:
                self.site_custom_facade.create_new_site(
                    domain=self.test_domain,
                    name="",
                    components=self.test_components,
                    template=self.test_template,
                    email=self.test_email
                )
            self.assertEqual(str(context.exception), ExceptionsEnum.INVALID_SITE_NAME.value)

            # Test invalid domain format
            with self.assertRaises(Exception) as context:
                self.site_custom_facade.create_new_site(
                    domain="invalid-domain",
                    name="Test Lab",
                    components=self.test_components,
                    template=self.test_template,
                    email=self.test_email
                )
            self.assertEqual(str(context.exception), ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)

            # Test invalid components format
            with self.assertRaises(Exception) as context:
                self.site_custom_facade.add_components_to_site(self.test_domain, "not-a-list")
            self.assertEqual(str(context.exception), ExceptionsEnum.INVALID_COMPONENTS_FORMAT.value)

    def test_get_site_by_domain(self):
        """Test getting site by domain."""
        with patch.object(self.site_custom_facade, 'sites', {self.test_domain: self.test_site}):
            result = self.site_custom_facade.get_site_by_domain(self.test_domain)
            self.assertIsNotNone(result)
            self.assertEqual(result.domain, self.test_domain)
            self.assertEqual(result.name, self.test_site.name)
            self.assertEqual(result.components, self.test_site.components)
            self.assertEqual(result.template, self.test_site.template)
            self.assertEqual(result.site_creator_email, self.test_site.site_creator_email)

if __name__ == '__main__':
    unittest.main() 