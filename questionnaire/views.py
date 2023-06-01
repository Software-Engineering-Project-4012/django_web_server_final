from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import QuestionnaireTemplateSerializer, QuestionnaireSerializer
from .models import QuestionnaireTemplate, Questionnaire, Submission
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from question.models import Question


class QuestionnaireTemplateListCreateView(generics.ListCreateAPIView):
    search_fields = ['template_name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = QuestionnaireTemplateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return QuestionnaireTemplate.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class QuestionnaireTemplateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionnaireTemplateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return QuestionnaireTemplate.objects.filter(creator=self.request.user)

    def delete(self, request, pk=None):
        instance = QuestionnaireTemplate.objects.filter(id=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionnaireList(generics.ListCreateAPIView):
    search_fields = ['employee__first_name', 'employee__last_name', 'deadline', 'template__template_name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Questionnaire.objects.filter(template__creator=self.request.user)
        return self.request.user.users.all()


class QuestionnaireDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Questionnaire.objects.filter(creator=self.request.user)

    def delete(self, request, pk=None):
        instance = QuestionnaireTemplate.objects.filter(id=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubmissionQuestionnaireGet(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        questionnaire_id = get_object_or_404(Questionnaire, id=request.GET.get('id'))
        submissions = Submission.objects.filter(questionnaire=questionnaire_id).values()

        return Response({'submissions': submissions}, status=status.HTTP_200_OK)


class SubmissionQuestionnaireCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        questionnaire_id = get_object_or_404(Questionnaire, id=request.data.get('questionnaire'))
        user_id = request.data.get('user')
        user = questionnaire_id.users.get(id=user_id)
        submission = Submission.objects.create(questionnaire=questionnaire_id, user=user,
                                               answers=request.data.get('answers'))
        submission.save()
        return Response({'message': 'submission created successfully!', 'id': submission.id},
                        status=status.HTTP_201_CREATED)


class SubmissionQuestionnaireDelete(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        questionnaire_id = get_object_or_404(Questionnaire, id=request.GET.get('questionnaire_id'))
        submissions = Submission.objects.filter(questionnaire=questionnaire_id)
        for submission in submissions:
            submission.delete()

        return Response({"message": f"submissions for questionnaire with id:{questionnaire_id} deleted successfully!"},
                        status=status.HTTP_204_NO_CONTENT)


class UserNotRespondedSubmission(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        questionnaire = get_object_or_404(Questionnaire, id=request.GET.get('id'))
        users = questionnaire.users.all().exclude(users__in=Submission.objects.filter(questionnaire=questionnaire).values().values_list('user', flat=True)).values()
        return Response({'users_not_responded': users}, status=status.HTTP_200_OK)


class GetNumberQuestions(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        questions = Question.objects.filter(template__id=request.GET.get('id')).values()
        return Response({'number_questions': len(questions)}, status=status.HTTP_200_OK)
