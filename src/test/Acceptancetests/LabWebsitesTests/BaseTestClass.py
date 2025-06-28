import unittest
from unittest.mock import patch

class BaseTestClass(unittest.TestCase):
    def setUp(self):
        # Start patchers for both UserFacade.get_email_from_token methods
        self.patcher_lab = patch(
            'src.main.DomainLayer.LabWebsites.User.UserFacade.UserFacade.get_email_from_token',
            side_effect=lambda *args, **kwargs: args[0] if args else kwargs.get('google_token')
        )
        self.patcher_gen = patch(
            'src.main.DomainLayer.LabGenerator.User.UserFacade.UserFacade.get_email_from_token',
            side_effect=lambda *args, **kwargs: args[0] if args else kwargs.get('google_token')
        )
        self.mock_lab = self.patcher_lab.start()
        self.mock_gen = self.patcher_gen.start()

    def tearDown(self):
        self.patcher_lab.stop()
        self.patcher_gen.stop() 