from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from questionnaire.models import QuestionnaireTemplate
from .models import Question


# Create your views here.

class CreateQuestionView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        question_type = request.data.get('type')
        question_text = request.data.get('question')
        template_id = request.data.get('template_id')
        template = QuestionnaireTemplate.objects.get(id=template_id)
        question_position = request.data.get('number')
        style = request.data.get('style')
        rows = request.data.get('rows')
        options = request.data.get('options')
        question = Question.objects.create(template=template, question_text=question_text,
                                           question_position=question_position, question_type=question_type,
                                           style=style, rows=rows, options=options)
        question.save()
        return Response({'message': 'Question created successfully', 'id': question.id}, status=status.HTTP_201_CREATED)


class GetQuestionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        template_id = request.query_params.get('template_id')
        questions = Question.objects.filter(template=template_id).values()
        return Response({'questions': questions}, status=status.HTTP_200_OK)


class DeleteQuestionView(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        question = Question.objects.get(id=request.data.get('question_id'))
        question.delete()
        return Response({'message': 'Question deleted successfully'}, status=status.HTTP_200_OK)


class EditQuestionView(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        question = Question.objects.get(id=request.data.get('question_id'))

        question.question_type = request.data.get('type', question.question_type)
        question.question_text = request.data.get('question', question.question_text)
        question.template_id = request.data.get('template_id', question.template_id)

        question.template = QuestionnaireTemplate.objects.get(id=question.template_id)
        question.question_position = request.data.get('number', question.question_position)
        question.style = request.data.get('style', question.style)
        question.rows = request.data.get('rows', question.rows)
        question.options = request.data.get('options', question.options)
        question.save()

        return Response({"message": "Question edited successfully!"}, status=status.HTTP_200_OK)
