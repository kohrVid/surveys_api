from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
