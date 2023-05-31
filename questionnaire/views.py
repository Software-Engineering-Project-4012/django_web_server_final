from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import QuestionnaireTemplateSerializer, QuestionnaireSerializer
from .models import QuestionnaireTemplate, Questionnaire
from rest_framework import filters


class QuestionnaireTemplateListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionnaireTemplateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return QuestionnaireTemplate.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class QuestionnaireTemplateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionnaireTemplateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return QuestionnaireTemplate.objects.filter(creator=self.request.user)


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
