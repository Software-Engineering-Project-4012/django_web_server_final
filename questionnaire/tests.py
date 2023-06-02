from django.test import TestCase
from rest_framework.test import APIClient
import datetime
import json
from .models import *
from question.models import Question


# Create your tests here.

class QuestionnaireTest(TestCase):
    def setUp(self) -> None:
        self.user_test = CustomUser.objects.create_user(username='test', password='test', first_name='kian',
                                                        last_name='majlessi', faculty='ce',
                                                        email='kianmajl@gmail.com', role='emp', position='ceo')

        self.user_admin_test = CustomUser.objects.create_superuser(username='test_admin', password='test_admin',
                                                                   first_name='audry', last_name='ebrahimi',
                                                                   faculty='ce', role='emp',
                                                                   position='Training Manager', email='audry@gmail.com')

        qt = QuestionnaireTemplate.objects.create(template_name='پرسشنامه کیان', description='نداریم',
                                                  creator=self.user_admin_test)

        Question.objects.create(template=qt, question_text='test', question_type='short_answer', question_position=1)

        Questionnaire.objects.create(employee=self.user_test, deadline='2023-12-02', template_id=1)
        Questionnaire.objects.get(id=1).users.add(self.user_test)

        Questionnaire.objects.create(employee=self.user_test, deadline='2023-12-12', template_id=1)
        Questionnaire.objects.get(id=2).users.add(self.user_test)

        Submission.objects.create(questionnaire_id=1, user_id=self.user_test.id,
                                  date='2021-06-01', answers=json.dumps({'1': 'test', '2': 'test'}))

        self.client_rest_admin = APIClient()
        response = self.client.post('/accounts/login/', data={'username': 'test_admin', 'password': 'test_admin'})
        self.client_rest_admin.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

        self.client_rest_user = APIClient()
        response = self.client.post('/accounts/login/', data={'username': 'test', 'password': 'test'})
        self.client_rest_user.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_create_questionnaire_template(self):
        response = self.client_rest_admin.post('/questionnaire/questionnaire_templates/',
                                               data={'template_name': 'پرسشنامه شخصی', 'description': 'test',
                                                     'creator': self.user_admin_test.id})
        self.assertEqual(response.status_code, 201)
        id_obj = response.data['id']
        self.assertEqual(QuestionnaireTemplate.objects.get(id=id_obj).template_name, 'پرسشنامه شخصی')
        self.assertEqual(QuestionnaireTemplate.objects.get(id=id_obj).description, 'test')
        self.assertEqual(QuestionnaireTemplate.objects.get(id=id_obj).creator, self.user_admin_test)

    def test_get_questionnaire_template_list(self):
        response = self.client_rest_admin.get('/questionnaire/questionnaire_templates/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['template_name'], 'پرسشنامه کیان')
        self.assertEqual(response.data[0]['description'], 'نداریم')
        self.assertEqual(response.data[0]['creator'], self.user_admin_test.id)

    def test_create_questionnaire(self):
        response = self.client_rest_admin.post('/questionnaire/questionnaires/',
                                               data={'employee': self.user_test.id, 'deadline': '2025-01-23',
                                                     'template': 1, 'users': [self.user_test.id]})
        self.assertEqual(response.status_code, 201)
        id_obj = response.data['id']
        self.assertEqual(Questionnaire.objects.get(id=id_obj).employee, self.user_test)
        self.assertEqual(Questionnaire.objects.get(id=id_obj).deadline.strftime('%Y-%m-%d'), '2025-01-23')
        self.assertEqual(Questionnaire.objects.get(id=id_obj).template.id, 1)
        self.assertEqual(Questionnaire.objects.get(id=id_obj).users.all()[0], self.user_test)

    def test_get_questionnaire_list(self):
        response = self.client_rest_admin.get('/questionnaire/questionnaires/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['employee'], self.user_test.get_full_name())
        self.assertEqual(response.data[0]['deadline'], '1402/09/11')
        questionnaire = Questionnaire.objects.get(id=1)
        self.assertEqual(response.data[0]['template'], questionnaire.template.template_name)
        self.assertEqual(response.data[0]['users'][0], self.user_test.id)

    def test_get_submissions(self):
        response = self.client_rest_admin.get('/questionnaire/submissions/get/', data={'id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['submissions']), 1)
        self.assertEqual(response.data['submissions'][0]['questionnaire_id'], 1)
        self.assertEqual(response.data['submissions'][0]['user_id'], self.user_test.id)
        self.assertEqual(response.data['submissions'][0]['date'], '1402/09/11')
        self.assertEqual(json.loads(response.data['submissions'][0]['answers']), {'1': 'test', '2': 'test'})

    def test_create_submission(self):
        response = self.client_rest_user.post('/questionnaire/submissions/create/',
                                              data={'questionnaire': 2, 'user': self.user_test.id,
                                                    'answers': json.dumps({'1': 'test', '2': 'test'})})

        self.assertEqual(response.status_code, 201)
        id_obj = response.data['id']
        self.assertEqual(Submission.objects.get(id=id_obj).questionnaire_id, 2)
        self.assertEqual(Submission.objects.get(id=id_obj).user_id, self.user_test.id)
        self.assertEqual(Submission.objects.get(id=id_obj).date.strftime('%Y-%m-%d'),
                         datetime.datetime.now().strftime('%Y-%m-%d'))
        self.assertEqual(json.loads(Submission.objects.get(id=id_obj).answers), {'1': 'test', '2': 'test'})

    def test_user_not_responded_submissions(self):
        response = self.client_rest_admin.get('/questionnaire/submissions/not-responded-users/', data={'id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users_not_responded']), 0)

    def test_number_of_questions_per_questionnaire_template(self):
        response = self.client_rest_admin.get('/questionnaire/questionnaires/number_questions/', data={'id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['number_questions'], 1)
