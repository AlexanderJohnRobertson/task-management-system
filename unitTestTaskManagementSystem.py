import unittest
from app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_login(self):
        response = self.app.get('login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log', response.data)

    def test_create_account(self):
        response = self.app.get('createaccount')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create', response.data)

    def test_add_task(self):
        response = self.app.get('addtask')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)


if __name__ == '__main__':
    unittest.main()