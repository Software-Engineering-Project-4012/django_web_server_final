from django.urls import path
from .views import *

urlpatterns = [
    path('questionnaire_templates/', QuestionnaireTemplateListCreateView.as_view()),
    path('questionnaire_template/<int:pk>/', QuestionnaireTemplateRetrieveUpdateDestroyView.as_view()),
    path('questionnaires/', QuestionnaireList.as_view()),
    path('questionnaires/<int:pk>/', QuestionnaireDetail.as_view()),
    path('questionnaires/number_questions/<int:pk>/', GetNumberQuestions.as_view()),
]
