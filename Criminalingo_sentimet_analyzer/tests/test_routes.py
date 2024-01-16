import unittest
from Criminalingo_sentimet_analyzer.app import app

class RoutesTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_analyze_route(self):
        response = self.app.post('/analyze', data={'tweet_text': 'Test tweet'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sentiment Analysis Result', response.data)

    def test_invalid_login(self):
        response = self.app.post('/login', data={'username': 'invalid', 'password': 'invalid'})
        self.assertIn(b'Invalid username/password', response.data)

if __name__ == '__main__':
    unittest.main()
