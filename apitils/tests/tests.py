from django.test import TestCase
from django.test.client import RequestFactory

from .models import Person
from .views import APIView


class ApitilsModelsTests(TestCase):
    def test_serialize_manager_applied(self):
        Person.objects.all().serialize()

    def test_serialize(self):
        person = Person.objects.create(first_name='John', last_name='Smith')
        self.assertEqual(
            person.serialize(),
            {'first_name': 'John', 'id': 1, 'last_name': 'Smith'}
        )


class ApitilsViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_ok(self):
        request = self.factory.get('/apiview/')
        response = APIView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_ok(self):
        request = self.factory.post('/apiview/', {'foo': 'bar'})
        response = APIView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '{"foo": "bar"}')

    def test_put_ok(self):
        request = self.factory.put(
            '/apiview/',
            '{"foo": "bar"}',
            content_type='application/json'
        )
        response = APIView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '{"foo": "bar"}')
