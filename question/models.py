from django.db import models
from questionnaire.models import QuestionnaireTemplate


class Question(models.Model):
    class StyleChoices(models.TextChoices):
        BOLD = 'bold', 'Bold'
        ITALIC = 'italic', 'Italic'
        UNDERLINE = 'underline', 'Underline'

    class QuestionType(models.TextChoices):
        SHORT_ANSWER = 'short_answer', 'Short Answer'
        MATRIX = 'matrix', 'Matrix'
        MULTIPLE_CHOICE = 'multiple_choice', 'Multiple Choice'

    template = models.ForeignKey(QuestionnaireTemplate, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    question_position = models.IntegerField()
    question_type = models.CharField(max_length=200, choices=QuestionType.choices, default=QuestionType.SHORT_ANSWER)
    style = models.CharField(max_length=200, null=True, blank=True, choices=StyleChoices.choices)
    rows = models.JSONField(null=True, blank=True)
    options = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.question_text
