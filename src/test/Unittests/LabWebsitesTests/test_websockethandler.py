import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

patcher = patch('src.main.DomainLayer.socketio_instance.socketio', autospec=True)
mock_socketio = patcher.start()
from src.main.DomainLayer.LabWebsites.Notifications.WebSocketHandler import WebSocketHandler

class TestWebSocketHandler(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        patcher.stop()

    def setUp(self):
        WebSocketHandler._instance = None
        self.handler = WebSocketHandler()
        self.handler.socketio = mock_socketio
        mock_socketio.reset_mock()

    def test_singleton_pattern(self):
        handler1 = WebSocketHandler()
        handler2 = WebSocketHandler()
        self.assertIs(handler1, handler2)

    def test_register_user(self):
        self.handler.register_user('user@example.com', 'lab.example.com', 'sid123')
        self.assertIn('lab.example.com', self.handler.connected_users)
        self.assertIn('user@example.com', self.handler.connected_users['lab.example.com'])
        self.assertEqual(self.handler.connected_users['lab.example.com']['user@example.com'], 'sid123')

    def test_register_multiple_users_same_domain(self):
        self.handler.register_user('user1@example.com', 'lab.example.com', 'sid1')
        self.handler.register_user('user2@example.com', 'lab.example.com', 'sid2')
        users = self.handler.connected_users['lab.example.com']
        self.assertEqual(users['user1@example.com'], 'sid1')
        self.assertEqual(users['user2@example.com'], 'sid2')

    def test_register_users_different_domains(self):
        self.handler.register_user('user@example.com', 'lab1.example.com', 'sid1')
        self.handler.register_user('user@example.com', 'lab2.example.com', 'sid2')
        self.assertIn('lab1.example.com', self.handler.connected_users)
        self.assertIn('lab2.example.com', self.handler.connected_users)
        self.assertEqual(self.handler.connected_users['lab1.example.com']['user@example.com'], 'sid1')
        self.assertEqual(self.handler.connected_users['lab2.example.com']['user@example.com'], 'sid2')

    def test_unregister_user_by_sid(self):
        self.handler.register_user('user@example.com', 'lab.example.com', 'sid123')
        self.handler.unregister_user_by_sid('sid123')
        self.assertNotIn('lab.example.com', self.handler.connected_users)

    def test_unregister_user_removes_empty_domain(self):
        self.handler.register_user('user@example.com', 'lab.example.com', 'sid123')
        self.handler.unregister_user_by_sid('sid123')
        self.assertNotIn('lab.example.com', self.handler.connected_users)

    def test_unregister_user_nonexistent_sid(self):
        self.handler.register_user('user@example.com', 'lab.example.com', 'sid123')
        self.handler.unregister_user_by_sid('nonexistent_sid')
        self.assertIn('user@example.com', self.handler.connected_users['lab.example.com'])

    def test_emit_to_user_connected(self):
        self.handler.register_user('user@example.com', 'lab.example.com', 'sid123')
        self.handler.emit_to_user('lab.example.com', 'user@example.com', 'test_event', {'data': 'test'})
        mock_socketio.emit.assert_called_once_with('test_event', {'data': 'test'}, to='sid123')

    def test_emit_to_user_not_connected(self):
        self.handler.emit_to_user('lab.example.com', 'user@example.com', 'test_event', {'data': 'test'})
        mock_socketio.emit.assert_not_called()

    def test_emit_to_all_in_domain(self):
        self.handler.register_user('user1@example.com', 'lab.example.com', 'sid1')
        self.handler.register_user('user2@example.com', 'lab.example.com', 'sid2')
        self.handler.emit_to_all_in_domain('lab.example.com', 'test_event', {'data': 'test'})
        self.assertEqual(mock_socketio.emit.call_count, 2)
        calls = mock_socketio.emit.call_args_list
        self.assertEqual(calls[0][0][0], 'test_event')
        self.assertEqual(calls[0][0][1], {'data': 'test'})
        self.assertEqual(calls[0][1]['to'], 'sid1')
        self.assertEqual(calls[1][1]['to'], 'sid2')

    def test_emit_to_all_in_domain_empty(self):
        self.handler.emit_to_all_in_domain('lab.example.com', 'test_event', {'data': 'test'})
        mock_socketio.emit.assert_not_called()

if __name__ == '__main__':
    unittest.main()