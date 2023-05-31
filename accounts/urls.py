from django.urls import path
from .views import *

urlpatterns = [
    path('login/', CustomAuthToken.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
    path('change-email/', ChangeEmailAPIView.as_view()),
    path('get-emp/', GetEmployeeListAPIView.as_view()),
    path('add-emp/', AddEmployeeAPIView.as_view()),
    path('edit-emp/', EditEmployeeAPIView.as_view()),
    path('delete-emp/', DeleteEmployeeAPIView.as_view()),
    path('get-stu/', GetStudentsListAPIView.as_view()),
    path('edit-stu/', EditStudentAPIView.as_view()),
    path('forget-password/', ForgetPasswordAPIView.as_view()),
]
