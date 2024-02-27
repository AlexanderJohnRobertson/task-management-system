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

    def test_view_task(self):
        response = self.app.get('viewtasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_update_task(self):
        response = self.app.get('updatetask')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_delete_task(self):
        response = self.app.get('deletetask')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_create_project(self):
        response = self.app.get('addproject')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_view_projects(self):
        response = self.app.get('viewprojects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_update_project(self):
        response = self.app.get('updateproject')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_delete_project(self):
        response = self.app.get('deleteproject')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_account_details(self):
        response = self.app.get('accountdetails')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_update_account_details(self):
        response = self.app.get('updateaccountdetails')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_change_username(self):
        response = self.app.get('changeusername')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_change_password(self):
        response = self.app.get('changepassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_view_account_details(self):
        response = self.app.get('accountdetails')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_user_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'', response.data)

    def test_user_home(self):
        response = self.app.get('userhome/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'', response.data)




if __name__ == '__main__':
    unittest.main()