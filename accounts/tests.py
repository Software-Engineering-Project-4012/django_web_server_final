from django.test import TestCase


# Create your tests here.

class AccountTest(TestCase):

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)