from django.db import models
from django.utils import timezone
from accounts.models import CustomUser


class QuestionnaireTemplate(models.Model):
    template_name = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.template_name


class Questionnaire(models.Model):
    template = models.ForeignKey(QuestionnaireTemplate, on_delete=models.CASCADE)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employee')
    deadline = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField(CustomUser, related_name='users')

    def __str__(self):
        return f'{str(self.template)} for {self.employee.username}'


class Submission(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    answers = models.JSONField()

    def __str__(self):
        return f'{str(self.questionnaire)} by {self.user.username}'