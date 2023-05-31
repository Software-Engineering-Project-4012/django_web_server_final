from django.db import models

from django.contrib.auth.models import AbstractUser

from .validators import phone_validator

import string
import secrets


class CustomUser(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNSET = 'MF', 'Unset'

    class Role(models.TextChoices):
        STUDENT = 'stu', 'Student'
        EMPLOYEE = 'emp', 'Employee'

    role = models.CharField(max_length=3, choices=Role.choices, default=Role.STUDENT)
    position = models.CharField(max_length=1000, blank=True)
    faculty = models.CharField(max_length=1000, blank=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.UNSET)
    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    image_path = request.data.get("image_path")
    def __str__(self):
        return self.username

    @staticmethod
    def make_random_password():
        password = ""
        for _ in range(4):
            password += secrets.choice(string.ascii_lowercase)
        password += secrets.choice(string.ascii_uppercase)
        password += secrets.choice(string.digits)
        return password
