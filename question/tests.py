from django.test import TestCase
from rest_framework.test import APIClient
from .models import Question
from questionnaire.models import QuestionnaireTemplate
from accounts.models import CustomUser
import json


class QuestionTest(TestCase):

    def setUp(self) -> None:
        self.user_admin_test = CustomUser.objects.create_superuser(username='test_admin', password='test_admin',
                                                                   first_name='audry', last_name='ebrahimi',
                                                                   faculty='ce', role='emp',
                                                                   position='Training Manager', email='audry@gmail.com')

        self.user_test = CustomUser.objects.create_user(username='test', password='test', first_name='kian',
                                                        last_name='majlessi', faculty='ce',
                                                        email='kianmajl@gmail.com', role='emp', position='ceo')

        self.template_1 = QuestionnaireTemplate.objects.create(template_name="Template_1", creator=self.user_admin_test)
        self.question_1 = Question.objects.create(
            template=self.template_1,
            question_text="Sample question",
            question_position=1,
            question_type=Question.QuestionType.SHORT_ANSWER,
            style=Question.StyleChoices.BOLD,
            rows=json.dumps(None),
            options=json.dumps({'min': 1, 'max': 100})
        )

        self.client_rest_admin = APIClient()
        response = self.client.post('/accounts/login/', data={'username': 'test_admin', 'password': 'test_admin'})
        self.client_rest_admin.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

        self.client_rest_user = APIClient()
        response = self.client.post('/accounts/login/', data={'username': 'test', 'password': 'test'})
        self.client_rest_user.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_create_question(self):
        response = self.client_rest_admin.post('/question/create/', data={
            'template_id': self.template_1.id,
            'question': 'Test_1 question',
            'number': 2,
            'type': Question.QuestionType.MULTIPLE_CHOICE,
            'style': Question.StyleChoices.BOLD,
            'rows': json.dumps(None),
            'options': json.dumps(['Option 1', 'Option 2'])
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Question created successfully')

        question = Question.objects.get(id=response.data['id'])
        self.assertEqual(question.question_text, 'Test_1 question')
        self.assertEqual(question.question_position, 2)
        self.assertEqual(question.question_type, Question.QuestionType.MULTIPLE_CHOICE)
        self.assertEqual(question.style, Question.StyleChoices.BOLD)
        self.assertEqual(json.loads(question.rows), None)
        self.assertEqual(json.loads(question.options), ['Option 1', 'Option 2'])

        response = self.client_rest_admin.post('/question/create/', data={
            'template_id': self.template_1.id,
            'question': 'Test_2 question',
            'number': 3,
            'type': Question.QuestionType.MATRIX,
            'style': Question.StyleChoices.ITALIC,
            'rows': json.dumps(['Row 1', 'Row 2']),
            'options': json.dumps(['Option 1', 'Option 2'])
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Question created successfully')
        question2 = Question.objects.get(id=response.data['id'])
        self.assertEqual(question2.question_text, 'Test_2 question')
        self.assertEqual(question2.question_position, 3)
        self.assertEqual(question2.question_type, Question.QuestionType.MATRIX)
        self.assertEqual(question2.style, Question.StyleChoices.ITALIC)
        self.assertEqual(json.loads(question2.rows), ['Row 1', 'Row 2'])
        self.assertEqual(json.loads(question2.options), ['Option 1', 'Option 2'])

    def test_get_question(self):
        response = self.client_rest_user.get('/question/get/', data={'template_id': self.template_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['questions']), 1)
        self.assertEqual(response.data['questions'][0]['question_text'], 'Sample question')
        self.assertEqual(response.data['questions'][0]['question_position'], 1)
        self.assertEqual(response.data['questions'][0]['question_type'], Question.QuestionType.SHORT_ANSWER)
        self.assertEqual(response.data['questions'][0]['style'], Question.StyleChoices.BOLD)
        self.assertEqual(json.loads(response.data['questions'][0]['rows']), None)
        self.assertEqual(json.loads(response.data['questions'][0]['options']), {'min': 1, 'max': 100})

    def test_delete_question(self):
        response = self.client_rest_admin.delete('/question/delete/', data={'question_id': self.question_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Question deleted successfully')
        self.assertFalse(Question.objects.filter(id=self.question_1.id).exists())

    def test_edit_question(self):
        response = self.client_rest_admin.put('/question/edit/', data={
            'question_id': self.question_1.id,
            'template_id': self.template_1.id,
            'question': 'Test_1 question',
            'number': 2,
            'type': Question.QuestionType.MULTIPLE_CHOICE,
            'style': Question.StyleChoices.BOLD,
            'rows': json.dumps(None),
            'options': json.dumps(['Option 1', 'Option 2'])
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Question edited successfully!')
        question = Question.objects.get(id=self.question_1.id)
        self.assertEqual(question.question_text, 'Test_1 question')
        self.assertEqual(question.question_position, 2)
        self.assertEqual(question.question_type, Question.QuestionType.MULTIPLE_CHOICE)
        self.assertEqual(question.style, Question.StyleChoices.BOLD)
        self.assertEqual(json.loads(question.rows), None)
        self.assertEqual(json.loads(question.options), ['Option 1', 'Option 2'])
