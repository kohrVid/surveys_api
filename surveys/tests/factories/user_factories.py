from django.contrib.auth.models import User, Group
from django_factory import factory
from faker import Faker

class UserFactory(factory.Factory):
    pk = 1
    username = Faker().name()
    password = 'Password1234!'
    url = "http://testserver/users/{}".format(pk)
    email = Faker().email()
    groups = []

    class Meta: 
        model = User

class GroupFactory(factory.Factory):
    pk = 1
    name = Faker().name()
    url = "http://testserver/groups/{}".format(pk)

    class Meta: 
        model = Group
