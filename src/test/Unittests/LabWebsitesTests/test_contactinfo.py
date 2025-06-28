import unittest
from src.main.DomainLayer.LabWebsites.Website.ContactInfo import ContactInfo

class TestContactInfo(unittest.TestCase):
    def setUp(self):
        self.contact_info = ContactInfo(
            lab_address='123 Main Street, City, Country',
            lab_mail='lab@example.com',
            lab_phone_num='123-456-7890'
        )

    def test_to_dict(self):
        contact_dict = self.contact_info.to_dict()
        self.assertEqual(contact_dict['address'], '123 Main Street, City, Country')
        self.assertEqual(contact_dict['email'], 'lab@example.com')
        self.assertEqual(contact_dict['phone_num'], '123-456-7890')

    def test_set_lab_address(self):
        self.contact_info.set_lab_address('456 Oak Avenue, Town, Country')
        self.assertEqual(self.contact_info.get_lab_address(), '456 Oak Avenue, Town, Country')

    def test_set_lab_mail(self):
        self.contact_info.set_lab_mail('newlab@example.com')
        self.assertEqual(self.contact_info.get_lab_mail(), 'newlab@example.com')

    def test_set_phone_num(self):
        self.contact_info.set_phone_num('987-654-3210')
        self.assertEqual(self.contact_info.get_lab_phone_num(), '987-654-3210')

if __name__ == '__main__':
    unittest.main() 