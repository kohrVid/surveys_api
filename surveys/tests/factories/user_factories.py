from django.contrib.auth.models import User, Group
from factory.django import DjangoModelFactory
from faker import Faker

class UserFactory(DjangoModelFactory):
    username = Faker().name()
    password = 'Password1234!'
    email = Faker().email()

    class Meta:
        model = User


class GroupFactory(DjangoModelFactory):
    name = Faker().name()

    class Meta:
        model = Group
