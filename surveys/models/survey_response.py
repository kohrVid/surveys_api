from django.db import models
from django.contrib.auth.models import User
from surveys.models.survey import Survey

class SurveyResponse(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    survey = models.ForeignKey(Survey, default=None, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(sr, survey_id, user_id):
        return sr(survey_id=survey_id, user_id=user_id)
