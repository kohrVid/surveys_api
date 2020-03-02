from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    name = models.CharField(max_length=255)
    available_places = models.IntegerField()
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)

    @classmethod
    def create(s, name, available_places, user_id):
      return s(name=name, available_places=available_places, user_id=user_id)

    def __str__(self):
        return self.name
