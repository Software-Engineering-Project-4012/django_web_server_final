from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import QuestionnaireTemplateSerializer, QuestionnaireSerializer
from .models import QuestionnaireTemplate, Questionnaire, Submission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import status


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
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        if self.request.user.is_staff:
            return Questionnaire.objects.filter(template__creator=self.request.user)
        return self.request.user.users.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class QuestionnaireDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return Questionnaire.objects.filter(creator=self.request.user)

    def delete(self, request, pk=None):
        instance = QuestionnaireTemplate.objects.filter(id=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SubmissionQuestionnaireGet(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, *args, **kwargs):
        questionnaire_id = Questionnaire.objects.get(id=request.GET.get('id'))
        submissions = Submission.objects.filter(questionnaire=questionnaire_id).values()

        return Response(context={'submissions': submissions}, status=status.HTTP_200_OK)


class SubmissionQuestionnaireDelete(APIView):
    permission_classes = (IsAdminUser, )

    def delete(self, request, *args, **kwargs):
        questionnaire_id = Questionnaire.objects.get(id=request.GET.get('id'))
        submissions = Submission.objects.filter(questionnaire=questionnaire_id)
        for submission in submissions:
            submission.delete()

        return Response({"message": f"submissions for questionnaire with id:{questionnaire_id} deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
