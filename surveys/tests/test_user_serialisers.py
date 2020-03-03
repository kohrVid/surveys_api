from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from surveys.serialisers.user_serialiser import UserSerialiser, GroupSerialiser
from surveys.tests.factories.user_factories import UserFactory, GroupFactory

class UserSerialiserTest(TestCase):
    def test_model_fields(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        user = UserFactory()

        serialiser_context = {
                'request': Request(request),
        }   
        
        for field_name in ['username', 'email']:
            self.assertEqual(
                UserSerialiser(
                    instance=user,
                    context=serialiser_context
                ).data[field_name],
                getattr(user, field_name)
            )

class GroupSerialiserTest(TestCase):
    def test_model_fields(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        group = GroupFactory()

        serialiser_context = {
                'request': Request(request),
        }   
        
        self.assertEqual(
            GroupSerialiser(
                instance=group,
                context=serialiser_context
            ).data['name'],
            getattr(group, 'name')
        )
