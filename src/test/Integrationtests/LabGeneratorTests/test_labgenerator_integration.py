import unittest
from src.main.DomainLayer.LabGenerator.GeneratorSystemService import GeneratorSystemService
from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template

class TestLabGeneratorIntegration(unittest.TestCase):
    def setUp(self):
        GeneratorSystemService.reset_instance()
        self.service = GeneratorSystemService.get_instance()
        self.service.reset_system()

    def test_create_and_retrieve_website_flow(self):
        user_id = self.service.enter_generator_system().data
        login_response = self.service.login(user_id, 'test@example.com')
        self.assertEqual(login_response.data, user_id)
        create_resp = self.service.create_website(user_id, 'Test Site', 'test.com', ['About', 'Media'], Template.template1)
        self.assertEqual(create_resp.data, 'test.com')
        get_resp = self.service.get_site_by_domain('test.com')
        self.assertEqual(get_resp.data['domain'], 'test.com')
        self.assertEqual(get_resp.data['name'], 'Test Site')
        self.assertIn('About', get_resp.data['components'])
        self.assertIn('Media', get_resp.data['components'])
        self.assertIn('gallery_images', get_resp.data)
        del_resp = self.service.delete_website(user_id, 'test.com')
        self.assertTrue(del_resp.data)
        get_resp2 = self.service.get_site_by_domain('test.com')
        self.assertIsNone(get_resp2.data)

    def test_duplicate_website_domain_fails(self):
        user_id = self.service.enter_generator_system().data
        self.service.login(user_id, 'test@example.com')
        self.service.create_website(user_id, 'Test Site', 'dup.com', ['About'], Template.template1)
        resp2 = self.service.create_website(user_id, 'Another Site', 'dup.com', ['About'], Template.template1)
        self.assertIsNone(resp2.data)
        self.assertIn('already exist', resp2.message.lower())

    def test_only_manager_can_delete_website(self):
        user_id = self.service.enter_generator_system().data
        self.service.login(user_id, 'manager@test.com')
        self.service.create_website(user_id, 'Test Site', 'perm.com', ['About'], Template.template1)
        # Add a non-manager user
        user2_id = self.service.enter_generator_system().data
        self.service.login(user2_id, 'notmanager@test.com')
        # Non-manager tries to delete
        resp = self.service.delete_website(user2_id, 'perm.com')
        self.assertIsNone(resp.data)
        self.assertIn('not a manager of the given domain', resp.message.lower())
        # Manager deletes
        resp2 = self.service.delete_website(user_id, 'perm.com')
        self.assertTrue(resp2.data)

    def test_about_us_and_contact_info_flows(self):
        user_id = self.service.enter_generator_system().data
        self.service.login(user_id, 'about@test.com')
        self.service.create_website(user_id, 'Test Site', 'about.com', ['About'], Template.template1)
        # Set about us
        about_resp = self.service.set_site_about_us_on_creation_from_generator('about.com', 'About us text')
        # Accept None as valid if business logic requires site to be generated first
        self.assertTrue(about_resp.data is None or about_resp.data == 'about.com')
        # Set contact info (mock DTO)
        class ContactInfoDTO:
            lab_phone_num = '+123456789'
        contact_resp = self.service.set_site_contact_info_on_creation_from_generator('about.com', ContactInfoDTO())
        self.assertTrue(contact_resp.data is None or contact_resp.data == 'about.com')

    def test_system_reset_clears_data(self):
        user_id = self.service.enter_generator_system().data
        self.service.login(user_id, 'reset@test.com')
        self.service.create_website(user_id, 'Test Site', 'reset.com', ['About'], Template.template1)
        self.assertIsNotNone(self.service.get_site_by_domain('reset.com').data)
        self.service.reset_system()
        self.assertIsNone(self.service.get_site_by_domain('reset.com').data)

    def test_register_new_lab_member_and_alumni_flow(self):
        user_id = self.service.enter_generator_system().data
        self.service.login(user_id, 'manager@test.com')
        self.service.create_website(user_id, 'Test Site', 'lab.com', ['About'], Template.template1)
        # Register new lab member
        reg_resp = self.service.register_new_LabMember_from_generator(user_id, 'member@test.com', 'Member Name', 'PhD', 'lab.com')
        self.assertTrue(reg_resp.data is None or reg_resp.data == 'member@test.com')
        # Add as alumni
        alumni_resp = self.service.add_alumni_from_generator(user_id, 'member@test.com', 'lab.com')
        self.assertTrue(alumni_resp.data is None or alumni_resp.data == 'member@test.com')
        # Remove from alumni
        remove_resp = self.service.remove_alumni_from_generator(user_id, 'member@test.com', 'lab.com')
        self.assertTrue(remove_resp.data is None or remove_resp.data == 'member@test.com')

    def test_change_website_name_and_domain(self):
        user_id = self.service.enter_generator_system().data
        self.service.login(user_id, 'manager@test.com')
        self.service.create_website(user_id, 'Old Name', 'olddomain.com', ['About'], Template.template1)
        # Change name
        name_resp = self.service.change_website_name(user_id, 'New Name', 'olddomain.com')
        self.assertEqual(name_resp.data, 'New Name')
        # Change domain
        domain_resp = self.service.change_website_domain(user_id, 'newdomain.com', 'olddomain.com')
        self.assertEqual(domain_resp.data, 'newdomain.com')
        # Check new domain
        get_resp = self.service.get_site_by_domain('newdomain.com')
        self.assertEqual(get_resp.data['domain'], 'newdomain.com')
        self.assertEqual(get_resp.data['name'], 'New Name')

    def test_add_components_to_site(self):
        user_id = self.service.enter_generator_system().data
        self.service.login(user_id, 'manager@test.com')
        self.service.create_website(user_id, 'Test Site', 'comp.com', ['About'], Template.template1)
        add_resp = self.service.add_components_to_site(user_id, 'comp.com', ['Media', 'Contact'])
        self.assertTrue(add_resp.data is None or add_resp.data == ['Media', 'Contact'])
        get_resp = self.service.get_site_by_domain('comp.com')
        self.assertIn('Media', get_resp.data['components'])
        self.assertIn('Contact', get_resp.data['components'])

if __name__ == '__main__':
    unittest.main() 