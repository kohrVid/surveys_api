from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    name = models.CharField(max_length=255)
    available_places = models.IntegerField()
    user_id = models.ForeignKey(User, default=0, on_delete=models.DO_NOTHING)

    @classmethod
    def create(s, name, available_places):
      return s(name=name, available_places=available_places)

    def __str__(self):
        return self.name
