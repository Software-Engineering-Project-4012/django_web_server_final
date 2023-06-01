from django.urls import path
from .views import *

urlpatterns = [
    path('questionnaire_templates/', QuestionnaireTemplateListCreateView.as_view()),
    path('questionnaire_template/<int:pk>/', QuestionnaireTemplateRetrieveUpdateDestroyView.as_view()),
    path('questionnaires/', QuestionnaireList.as_view()),
    path('questionnaires/<int:pk>/', QuestionnaireDetail.as_view()),
    path('questionnaires/number_questions/', GetNumberQuestions.as_view()),
    path('submissions/get/', SubmissionQuestionnaireGet.as_view()),
    path('submissions/create/', SubmissionQuestionnaireCreate.as_view()),
    path('submissions/delete/', SubmissionQuestionnaireDelete.as_view()),
    path('submissions/not-responded-users/', UserNotRespondedSubmission.as_view()),
    path('submissions/export_excel/<int:id>/', ExportExcel.as_view()),
]
