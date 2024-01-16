import unittest
from Criminalingo_sentimet_analyzer.app import app

class UserAuthenticationTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_successful_login(self):
        response = self.app.post('/login', data={'username': 'admin', 'password': 'password'})
        self.assertIn(b'Successful login', response.data)

    def test_failed_login(self):
        response = self.app.post('/login', data={'username': 'invalid', 'password': 'invalid'})
        self.assertIn(b'Invalid username/password', response.data)

if __name__ == '__main__':
    unittest.main()
