import unittest

from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabGenerator.User.User import User

class TestSiteCustom(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_user = User("test_user")
        self.test_email = "test@example.com"
        self.test_template = Template.template1
        self.test_components = ["About", "Contact", "Publications"]
        self.test_site = SiteCustom(
            domain="test-lab.com",
            name="Test Lab",
            components=self.test_components,
            template=self.test_template,
            site_creator_email=self.test_email,
            logo=None,
            home_picture=None,
            generated=False,
            gallery_path=None
        )

    def test_site_creation(self):
        """Test site creation with valid data."""
        self.assertEqual(self.test_site.domain, "test-lab.com")
        self.assertEqual(self.test_site.name, "Test Lab")
        self.assertEqual(self.test_site.components, self.test_components)
        self.assertEqual(self.test_site.template, self.test_template)
        self.assertEqual(self.test_site.site_creator_email, self.test_email)
        self.assertFalse(self.test_site.generated)
        self.assertIsNone(self.test_site.logo)
        self.assertIsNone(self.test_site.home_picture)
        self.assertIsNone(self.test_site.gallery_path)

    def test_update_site_info(self):
        """Test updating site information."""
        new_name = "Updated Lab"
        new_domain = "updated-lab.com"
        self.test_site.change_name(new_name)
        self.test_site.change_domain(new_domain)
        self.assertEqual(self.test_site.name, new_name)
        self.assertEqual(self.test_site.domain, new_domain)

    def test_change_template(self):
        """Test changing site template."""
        new_template = Template.template2
        self.test_site.change_template(new_template)
        self.assertEqual(self.test_site.template, new_template)

    def test_add_components(self):
        """Test adding components to site."""
        new_components = ["Media", "News"]
        self.test_site.add_component(new_components)
        self.assertEqual(self.test_site.components, new_components)

    def test_remove_component(self):
        """Test removing component from site."""
        self.test_site.remove_component("About")
        self.assertNotIn("About", self.test_site.components)

    def test_set_generated(self):
        """Test setting site as generated."""
        self.test_site.set_generated()
        self.assertTrue(self.test_site.generated)

    def test_set_logo_and_home_picture(self):
        """Test setting logo and home picture."""
        logo = "logo.png"
        home_picture = "home.jpg"
        self.test_site.set_logo(logo)
        self.test_site.set_home_picture(home_picture)
        self.assertEqual(self.test_site.logo, logo)
        self.assertEqual(self.test_site.home_picture, home_picture)

    def test_site_serialization(self):
        """Test site serialization to DTO."""
        dto = self.test_site.to_dto()
        self.assertEqual(dto.domain, self.test_site.domain)
        self.assertEqual(dto.name, self.test_site.name)
        self.assertEqual(dto.template, self.test_site.template.value)
        self.assertEqual(dto.site_creator_email, self.test_site.site_creator_email)
        self.assertEqual(dto.generated, self.test_site.generated)
        self.assertEqual(dto.logo, self.test_site.logo)
        self.assertEqual(dto.home_picture, self.test_site.home_picture)
        self.assertEqual(dto.gallery_path, self.test_site.gallery_path)

if __name__ == '__main__':
    unittest.main() 