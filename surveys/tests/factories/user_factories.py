from django.contrib.auth.models import User, Group
from factory.django import DjangoModelFactory
from faker import Faker

class UserFactory(DjangoModelFactory):
    pk = 1
    username = Faker().name()
    password = 'Password1234!'
    url = "http://testserver/users/{}".format(pk)
    email = Faker().email()
    groups = []

    class Meta: 
        model = User

class GroupFactory(DjangoModelFactory):
    pk = 1
    name = Faker().name()
    url = "http://testserver/groups/{}".format(pk)

    class Meta: 
        model = Group
