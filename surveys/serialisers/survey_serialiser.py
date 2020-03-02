from rest_framework import serializers
from surveys.models.survey import Survey

class SurveySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['name', 'available_places', 'user_id']
