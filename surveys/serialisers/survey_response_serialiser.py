from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from surveys.models.survey import Survey
from surveys.models.survey_response import SurveyResponse

class SurveyResponseSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['id', 'survey_id', 'user_id', 'created_at']

    def create(self, validated_data):
        survey_id = self.context["request"].data["survey_id"]
        user_id = self.context["request"].data["user_id"]
        survey = Survey.objects.get(pk=survey_id)

        if survey.available_places > 0:
            survey_response = SurveyResponse.objects.create(
                    survey=survey,
                    user=User.objects.get(pk=user_id)
            )

            return survey_response

        raise ValidationError({
            "survey_id": ["No more available places for this survey"]
        })
