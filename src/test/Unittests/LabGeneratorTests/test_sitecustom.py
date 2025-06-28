import unittest
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template

class TestSiteCustom(unittest.TestCase):
    def setUp(self):
        self.site = SiteCustom(
            domain='lab.example.com',
            name='Lab Site',
            components=['Homepage', 'Contact Us'],
            template=Template.template1,
            site_creator_email='creator@example.com',
            logo='logo.png',
            home_picture='home.jpg',
            generated=False
        )

    def test_change_template(self):
        self.site.change_template(Template.template2)
        self.assertEqual(self.site.template, Template.template2)

    def test_add_component(self):
        new_components = ['Homepage', 'Contact Us', 'Research']
        self.site.add_component(new_components)
        self.assertEqual(self.site.components, new_components)
        with self.assertRaises(TypeError):
            self.site.add_component('Not a list')

    def test_remove_component(self):
        self.site.remove_component('Homepage')
        self.assertNotIn('Homepage', self.site.components)

    def test_change_name(self):
        self.site.change_name('New Name')
        self.assertEqual(self.site.name, 'New Name')

    def test_change_domain(self):
        self.site.change_domain('newdomain.com')
        self.assertEqual(self.site.domain, 'newdomain.com')

    def test_set_generated(self):
        self.site.set_generated()
        self.assertTrue(self.site.generated)

    def test_set_logo(self):
        self.site.set_logo('new_logo.png')
        self.assertEqual(self.site.logo, 'new_logo.png')

    def test_set_home_picture(self):
        self.site.set_home_picture('new_home.jpg')
        self.assertEqual(self.site.home_picture, 'new_home.jpg')

    def test_set_site_creator_email(self):
        self.site.set_site_creator_email('new_creator@example.com')
        self.assertEqual(self.site.site_creator_email, 'new_creator@example.com')

    def test_set_gallery_path(self):
        self.site.set_gallery_path('gallery/path')
        self.assertEqual(self.site.gallery_path, 'gallery/path')

if __name__ == '__main__':
    unittest.main() 