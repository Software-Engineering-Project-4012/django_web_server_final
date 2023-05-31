from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateQuestionView.as_view()),
    path('get/', GetQuestionsView.as_view()),
    path('delete/', DeleteQuestionView.as_view()),
    path('edit/', EditQuestionView.as_view()),
]
