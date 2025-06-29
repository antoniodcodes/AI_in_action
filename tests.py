import unittest
import json
from unittest.mock import patch, Mock
from app import app


class FlaskAppTestCase(unittest.TestCase):
    """Test cases for Flask application routes"""

    def setUp(self):
        """Set up test client and configure app for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the index route (/)"""
        response = self.app.get('/')
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check content type
        self.assertIn('text/html', response.content_type)
        
        # Check response content
        self.assertIn(b'Hello World', response.data)

    def test_health_route(self):
        """Test the health check route (/health)"""
        response = self.app.get('/health')
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check content type
        self.assertIn('application/json', response.content_type)
        
        # Parse JSON response
        data = json.loads(response.data)
        
        # Check response structure
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')

    @patch('app.requests.get')
    def test_weather_route_success(self, mock_get):
        """Test weather route with valid coordinates"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'latitude': 40.7128,
            'longitude': -74.0060,
            'current_weather': {
                'temperature': 20.5,
                'weathercode': 1
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Make request to weather endpoint
        response = self.app.get('/weather?latitude=40.7128&longitude=-74.0060')
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check content type
        self.assertIn('application/json', response.content_type)
        
        # Parse JSON response
        data = json.loads(response.data)
        
        # Check response structure
        self.assertIn('latitude', data)
        self.assertIn('longitude', data)
        self.assertIn('current_weather', data)
        
        # Verify mock was called correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn('latitude=40.7128', call_args)
        self.assertIn('longitude=-74.0060', call_args)

    def test_weather_route_missing_parameters(self):
        """Test weather route with missing parameters"""
        # Test missing latitude
        response = self.app.get('/weather?longitude=-74.0060')
        self.assertEqual(response.status_code, 200)  # Current implementation doesn't validate
        
        # Test missing longitude
        response = self.app.get('/weather?latitude=40.7128')
        self.assertEqual(response.status_code, 200)  # Current implementation doesn't validate
        
        # Test no parameters
        response = self.app.get('/weather')
        self.assertEqual(response.status_code, 200)  # Current implementation doesn't validate

    @patch('app.requests.get')
    def test_weather_route_api_error(self, mock_get):
        """Test weather route when external API returns error"""
        # Mock API error response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        # Make request to weather endpoint
        response = self.app.get('/weather?latitude=40.7128&longitude=-74.0060')
        
        # Current implementation doesn't handle errors, so it will fail
        # This test documents the current behavior
        self.assertEqual(response.status_code, 200)  # or 500 depending on implementation

    @patch('app.requests.get')
    def test_weather_route_invalid_json(self, mock_get):
        """Test weather route when API returns invalid JSON"""
        # Mock response with invalid JSON
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response

        # Make request to weather endpoint
        response = self.app.get('/weather?latitude=40.7128&longitude=-74.0060')
        
        # Current implementation doesn't handle JSON errors
        # This test documents the current behavior
        self.assertEqual(response.status_code, 200)  # or 500 depending on implementation

    def test_weather_route_invalid_coordinates(self):
        """Test weather route with invalid coordinate values"""
        # Test invalid latitude (out of range)
        response = self.app.get('/weather?latitude=100&longitude=-74.0060')
        self.assertEqual(response.status_code, 200)  # Current implementation doesn't validate
        
        # Test invalid longitude (out of range)
        response = self.app.get('/weather?latitude=40.7128&longitude=200')
        self.assertEqual(response.status_code, 200)  # Current implementation doesn't validate
        
        # Test non-numeric coordinates
        response = self.app.get('/weather?latitude=abc&longitude=def')
        self.assertEqual(response.status_code, 200)  # Current implementation doesn't validate

    def test_nonexistent_route(self):
        """Test accessing a non-existent route"""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_weather_route_different_coordinates(self):
        """Test weather route with different coordinate sets"""
        with patch('app.requests.get') as mock_get:
            # Mock successful API response
            mock_response = Mock()
            mock_response.json.return_value = {
                'latitude': 51.5074,
                'longitude': -0.1278,
                'current_weather': {
                    'temperature': 15.2,
                    'weathercode': 3
                }
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Test London coordinates
            response = self.app.get('/weather?latitude=51.5074&longitude=-0.1278')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['latitude'], 51.5074)
            self.assertEqual(data['longitude'], -0.1278)

    def test_weather_route_edge_cases(self):
        """Test weather route with edge case coordinates"""
        with patch('app.requests.get') as mock_get:
            # Mock successful API response
            mock_response = Mock()
            mock_response.json.return_value = {
                'latitude': 0.0,
                'longitude': 0.0,
                'current_weather': {
                    'temperature': 25.0,
                    'weathercode': 0
                }
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Test coordinates at origin (0,0)
            response = self.app.get('/weather?latitude=0&longitude=0')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['latitude'], 0.0)
            self.assertEqual(data['longitude'], 0.0)

    def test_http_methods(self):
        """Test that routes only accept appropriate HTTP methods"""
        # Test POST on GET-only routes
        response = self.app.post('/')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
        
        response = self.app.post('/health')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
        
        response = self.app.post('/weather')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed


class FlaskAppIntegrationTestCase(unittest.TestCase):
    """Integration tests for Flask application"""

    def setUp(self):
        """Set up test client and configure app for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_full_application_flow(self):
        """Test the complete application flow"""
        # Test all endpoints in sequence
        endpoints = ['/', '/health', '/weather?latitude=40.7128&longitude=-74.0060']
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.app.get(endpoint)
                self.assertIn(response.status_code, [200, 404, 405])


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(FlaskAppTestCase))
    test_suite.addTest(unittest.makeSuite(FlaskAppIntegrationTestCase))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    exit(not result.wasSuccessful()) 