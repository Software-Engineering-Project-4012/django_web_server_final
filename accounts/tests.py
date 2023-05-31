from django.test import TestCase
from rest_framework.test import APIClient
from .models import CustomUser


class AccountTest(TestCase):

    def setUp(self) -> None:
        self.user_test = CustomUser.objects.create_user(username='test', password='test', first_name='kian',
                                                        last_name='majlessi', faculty='ce',
                                                        email='kianmajl@gmail.com', role='emp', position='ceo')

        self.user_admin_test = CustomUser.objects.create_superuser(username='test_admin', password='test_admin',
                                                                   first_name='audry', last_name='ebrahimi',
                                                                   faculty='ce', role='emp',
                                                                   position='Training Manager', email='audry@gmail.com')

        CustomUser.objects.create_user(username='kianchi', password='test1', first_name='kian', last_name='majlessi',
                                       faculty='ce', position='anjoman', role='stu')

        self.client_rest_admin = APIClient()
        response = self.client.post('/accounts/login/', data={'username': 'test_admin', 'password': 'test_admin'})
        self.client_rest_admin.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

        self.client_rest_user = APIClient()
        response = self.client.post('/accounts/login/', data={'username': 'test', 'password': 'test'})
        self.client_rest_user.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_login(self):
        response = self.client.post('/accounts/login/', data={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user_full_name'], 'kian majlessi')
        self.assertEqual(response.data['is_staff'], False)

        response = self.client.post('/accounts/login/', data={'username': 'test_admin', 'password': 'test_admin'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user_full_name'], 'audry ebrahimi')
        self.assertEqual(response.data['is_staff'], True)

    def test_login_fail(self):
        response = self.client.post('/accounts/login/', data={'username': 'test', 'password': 'test1'})
        self.assertEqual(response.status_code, 400)

    def test_change_password(self):
        response = self.client_rest_user.put('/accounts/change-password/',
                                             data={'confirm_password': 'test1', 'old_password': 'test',
                                                   'new_password': 'test1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Password updated successfully!')
        response = self.client.post('/accounts/login/', data={'username': 'test', 'password': 'test1'})
        self.assertEqual(response.status_code, 200)

    def test_change_email(self):
        response = self.client_rest_user.put('/accounts/change-email/',
                                             data={'new_email': 'kianmajl@outlook.com',
                                                   'confirm_email': 'kianmajl@outlook.com'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Email updated successfully!')
        self.assertEqual(CustomUser.objects.get(username='test').email, 'kianmajl@outlook.com')

    def test_get_employee_list(self):
        response = self.client_rest_admin.get('/accounts/get-emp/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'employees': [
            {'username': 'test', 'name': 'kian majlessi', 'faculty': 'ce', 'position': 'ceo',
             'email': 'kianmajl@gmail.com'},
            {'username': 'test_admin', 'name': 'audry ebrahimi', 'faculty': 'ce', 'email': 'audry@gmail.com',
             'position': 'Training Manager'}]})

    def test_get_student_list(self):
        response = self.client_rest_admin.get('/accounts/get-stu/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(),
                             {'students': [{'username': 'kianchi', 'name': 'kian majlessi', 'email': '',
                                            'faculty': 'ce', 'position': 'anjoman'}]})

    def test_add_employee(self):
        response = self.client_rest_admin.post('/accounts/add-emp/',
                                               data={'username': 'test1', 'first_name': 'shaghayegh',
                                                     'last_name': 'shahbazi', 'faculty': 'ce', 'position': 'it',
                                                     'email': 'test@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Employee added successfully!')
        self.assertTrue(CustomUser.objects.filter(username='test1').exists())

    def test_edit_student(self):
        response = self.client_rest_admin.put('/accounts/edit-stu/',
                                              data={'username': 'kianchi', 'first_name': 'audry',
                                                    'phone': '09111111111'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Student updated successfully!')
        self.assertEqual(CustomUser.objects.get(username='kianchi').first_name, 'audry')
        self.assertEqual(CustomUser.objects.get(username='kianchi').phone, '09111111111')

    def test_delete_employee(self):
        response = self.client_rest_admin.delete('/accounts/delete-emp/', data={'username': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Employee deleted successfully!')
        self.assertFalse(CustomUser.objects.filter(username='test').exists())

    def test_edit_employee(self):
        response = self.client_rest_admin.put('/accounts/edit-emp/', data={'username': 'test', 'position': 'security'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Employee updated successfully!')
        self.assertEqual(CustomUser.objects.get(username='test').position, 'security')
        