import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the main directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../main')))

from DomainLayer.LabWebsites.Notifications.WebSocketHandler import WebSocketHandler

class TestWebSocketHandler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.handler = WebSocketHandler()

    def test_handler_initialization(self):
        """Test if handler initializes correctly."""
        self.assertIsNotNone(self.handler)
        self.assertIsInstance(self.handler.clients, set)

    def test_client_connection(self):
        """Test client connection handling."""
        mock_client = Mock()
        
        # Test adding client
        self.handler.add_client(mock_client)
        self.assertIn(mock_client, self.handler.clients)
        
        # Test removing client
        self.handler.remove_client(mock_client)
        self.assertNotIn(mock_client, self.handler.clients)

    def test_broadcast_message(self):
        """Test broadcasting messages to clients."""
        mock_client1 = Mock()
        mock_client2 = Mock()
        
        self.handler.add_client(mock_client1)
        self.handler.add_client(mock_client2)
        
        test_message = "Test Message"
        self.handler.broadcast(test_message)
        
        mock_client1.send.assert_called_once_with(test_message)
        mock_client2.send.assert_called_once_with(test_message)

    def test_handle_message(self):
        """Test message handling."""
        mock_client = Mock()
        test_message = "Test Message"
        
        with patch.object(self.handler, 'broadcast') as mock_broadcast:
            self.handler.handle_message(mock_client, test_message)
            mock_broadcast.assert_called_once_with(test_message)

    def test_error_handling(self):
        """Test error handling."""
        mock_client = Mock()
        mock_client.send.side_effect = Exception("Test Error")
        
        # Test that error doesn't crash the handler
        self.handler.add_client(mock_client)
        self.handler.broadcast("Test Message")
        
        # Client should be removed after error
        self.assertNotIn(mock_client, self.handler.clients)

if __name__ == '__main__':
    unittest.main() 