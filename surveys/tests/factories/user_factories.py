from django.contrib.auth.models import User, Group
from factory.django import DjangoModelFactory
from faker import Faker

class UserFactory(DjangoModelFactory):
    pk = 1
    username = Faker().name()
    password = 'Password1234!'
    email = Faker().email()

    class Meta:
        model = User


class GroupFactory(DjangoModelFactory):
    pk = 1
    name = Faker().name()

    class Meta:
        model = Group
