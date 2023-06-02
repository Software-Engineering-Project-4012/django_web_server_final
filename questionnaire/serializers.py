from rest_framework import serializers
from .models import QuestionnaireTemplate, Questionnaire
import jdatetime


class QuestionnaireTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireTemplate
        fields = '__all__'


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(QuestionnaireSerializer, self).to_representation(instance)
        rep['template'] = instance.template.template_name
        rep['employee'] = instance.employee.get_full_name()
        rep['deadline'] = jdatetime.datetime.fromgregorian(datetime=instance.deadline).strftime("%Y/%m/%d")
        return rep
