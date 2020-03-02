from django.contrib.auth.models import User
from rest_framework import serializers
from surveys.models.survey import Survey

class SurveySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'name', 'available_places', 'user_id']

    def create(self, validated_data):
        name=validated_data.get('name')
        available_places=validated_data.get('available_places')
        user_id = self.context["request"].data["user_id"]

        survey = Survey.objects.create(
                name=name,
                available_places=available_places,
                user=User.objects.get(pk=user_id)
        )

        return survey
