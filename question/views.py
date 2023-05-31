from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Question


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
        return Response({'message': 'Question created successfully'}, status=status.HTTP_201_CREATED)
