import unittest
from unittest.mock import patch, MagicMock, Mock
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustomFacade import SiteCustomFacade
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class TestSiteCustomFacade(unittest.TestCase):
    def setUp(self):
        SiteCustomFacade.reset_instance()
        self.facade = SiteCustomFacade()
        self.facade.dal_controller = Mock()
        self.facade.sites = {}

    def test_singleton(self):
        f1 = SiteCustomFacade.get_instance()
        f2 = SiteCustomFacade.get_instance()
        self.assertIs(f1, f2)

    def test_reset_instance(self):
        f1 = SiteCustomFacade.get_instance()
        SiteCustomFacade.reset_instance()
        f2 = SiteCustomFacade.get_instance()
        self.assertIsNot(f1, f2)

    def test_error_if_domain_is_not_valid(self):
        with self.assertRaises(Exception) as ctx:
            self.facade.error_if_domain_is_not_valid('invalid_domain')
        self.assertEqual(str(ctx.exception), ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)

    def test_change_site_domain(self):
        site = Mock()
        self.facade.sites['old.com'] = site
        self.facade.dal_controller.siteCustom_repo = Mock()
        self.facade.change_site_domain('old.com', 'new.com')
        self.assertIn('new.com', self.facade.sites)
        self.assertNotIn('old.com', self.facade.sites)
        site.change_domain.assert_called_once_with('new.com')
        self.facade.dal_controller.siteCustom_repo.save.assert_called()

    def test_set_custom_site_as_generated(self):
        site = Mock()
        self.facade.sites['d.com'] = site
        self.facade.dal_controller.siteCustom_repo = Mock()
        self.facade.set_custom_site_as_generated('d.com')
        site.set_generated.assert_called_once()
        self.facade.dal_controller.siteCustom_repo.save.assert_called()

    def test_set_logo(self):
        site = Mock()
        self.facade.sites['d.com'] = site
        self.facade.dal_controller.siteCustom_repo = Mock()
        self.facade.set_logo('d.com', 'logo.png')
        site.set_logo.assert_called_once_with('logo.png')
        self.facade.dal_controller.siteCustom_repo.save.assert_called()

    def test_set_home_picture(self):
        site = Mock()
        self.facade.sites['d.com'] = site
        self.facade.dal_controller.siteCustom_repo = Mock()
        self.facade.set_home_picture('d.com', 'home.png')
        site.set_home_picture.assert_called_once_with('home.png')
        self.facade.dal_controller.siteCustom_repo.save.assert_called()

    def test_get_site_by_domain(self):
        site = Mock()
        dto = Mock()
        site.to_dto.return_value = dto
        self.facade.sites['d.com'] = site
        with patch('src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustomDTO.SiteCustomDTO.from_site_custom', return_value=dto):
            result = self.facade.get_site_by_domain('d.com')
            self.assertEqual(result, dto)

    def test_delete_website(self):
        site = Mock()
        self.facade.sites['d.com'] = site
        self.facade.dal_controller.siteCustom_repo = Mock()
        self.facade.delete_website('d.com')
        self.assertNotIn('d.com', self.facade.sites)
        self.facade.dal_controller.siteCustom_repo.delete.assert_called_once_with('d.com')

    def test_reset_system(self):
        self.facade.sites = {'a.com': Mock(), 'b.com': Mock()}
        self.facade.dal_controller.drop_all_tables = Mock()
        self.facade.reset_system()
        self.assertEqual(self.facade.sites, {})
        self.facade.dal_controller.drop_all_tables.assert_called_once()

if __name__ == '__main__':
    unittest.main() 