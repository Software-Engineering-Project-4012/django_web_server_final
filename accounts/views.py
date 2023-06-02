from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from django.db.models import Q
from accounts.models import CustomUser
import ghasedakpack
import secrets

SMS_API = 'API_KEY'
LINE_NUMBER = 'LINE_NUMBER'


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_full_name': user.get_full_name(),
            'image_path': user.imagePath,
            'is_staff': user.is_staff
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.username}!'},
            status=status.HTTP_204_NO_CONTENT
        )


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not check_password(old_password, user.password):
            return Response({"message": "Old password do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)


class ChangeEmailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = request.user

        new_email = request.data.get("new_email")
        password = request.data.get("password")

        if not check_password(password, user.password):
            return Response({"message": "Password do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user.email = new_email
        user.save()

        return Response({"message": "Email updated successfully!"}, status=status.HTTP_200_OK)


class ChangePhoneAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = request.user

        new_phone = request.data.get("new_phone")
        password = request.data.get("password")

        if not check_password(password, user.password):
            return Response({"message": "Password do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user.phone = new_phone
        user.save()

        return Response({"message": "Phone updated successfully!"}, status=status.HTTP_200_OK)


class GetEmployeeListAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        employees = CustomUser.objects.filter(role='emp')
        search = self.request.query_params.get('search')
        if search is not None:
            employees = employees.filter(Q(first_name=search) | Q(last_name=search))
        data = []
        for employee in employees:
            data.append({
                "username": employee.username,
                "name": employee.get_full_name(),
                "email": employee.email,
                "faculty": employee.faculty,
                "position": employee.position,
                "phone": employee.phone,
            })
        return Response(data, status=status.HTTP_200_OK)


class AddEmployeeAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        username = request.data.get("username")
        email = request.data.get("email")
        faculty = request.data.get("faculty")
        position = request.data.get("position")
        role = 'emp'
        phone = request.data.get("phone")
        password = CustomUser.objects.make_random_password()
        image_path = request.data.get("image_path")
        CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                       last_name=last_name, faculty=faculty, position=position, role=role, phone=phone, imagePath=image_path)
        return Response({"message": "Employee added successfully!", "user_pass": password}, status=status.HTTP_200_OK)


class EditEmployeeAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = CustomUser.objects.get(username=username)

        first_name = request.data.get("first_name", user.first_name)
        last_name = request.data.get("last_name", user.last_name)
        email = request.data.get("email", user.email)
        faculty = request.data.get("faculty", user.faculty)
        position = request.data.get("position", user.position)
        phone = request.data.get("phone", user.phone)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.faculty = faculty
        user.position = position
        user.phone = phone
        user.save()

        return Response({"message": "Employee updated successfully!"}, status=status.HTTP_200_OK)


class DeleteEmployeeAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        username = request.data.get("username")

        user = CustomUser.objects.get(username=username)
        user.delete()

        return Response({"message": "Employee deleted successfully!"}, status=status.HTTP_200_OK)


class GetStudentsListAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        students = CustomUser.objects.filter(role='stu')
        search = self.request.query_params.get('search')
        if search is not None:
            students = students.filter(Q(first_name=search) | Q(last_name=search))
        data = []
        for student in students:
            data.append({
                "username": student.username,
                "name": student.get_full_name(),
                "email": student.email,
                "faculty": student.faculty,
                "position": student.position,
                "phone": student.phone,
            })
        return Response(data, status=status.HTTP_200_OK)


class EditStudentAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = CustomUser.objects.get(username=username)

        first_name = request.data.get("first_name", user.first_name)
        last_name = request.data.get("last_name", user.last_name)
        email = request.data.get("email", user.email)
        faculty = request.data.get("faculty", user.faculty)
        position = request.data.get("position", user.position)
        phone = request.data.get("phone", user.phone)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.faculty = faculty
        user.position = position
        user.phone = phone
        user.save()

        return Response({"message": "Student updated successfully!"}, status=status.HTTP_200_OK)


class ForgetPasswordAPIView(APIView):

    def get(self, request, *args, **kwargs):
        number = request.GET.get("phone")

        sms = ghasedakpack.Ghasedak(SMS_API)

        password_length = 6
        sms_pass = secrets.token_urlsafe(password_length)
        sms_txt = f'Your new password is: {sms_pass}'
        if sms.send({f'message': {str(sms_txt)}, 'receptor': {str(number)}, 'linenumber': {str(LINE_NUMBER)}}):
            user = get_object_or_404(CustomUser, phone=number)
            user.set_password(sms_pass)
            user.save()
            return Response({"message": "Password sent and updated successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Error in sending sms!"}, status=status.HTTP_400_BAD_REQUEST)
class GetUsersListAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.filter(Q(role='stu') | Q(role='emp'))
        search = self.request.query_params.get('search')
        if search is not None:
            users = users.filter(Q(first_name=search) | Q(last_name=search))
        data = []
        for user in users:
            data.append({
                "username": user.username,
                "name": user.get_full_name(),
                "email": user.email,
                "faculty": user.faculty,
                "position": user.position,
                "phone": user.phone,
            })
        return Response(data, status=status.HTTP_200_OK)