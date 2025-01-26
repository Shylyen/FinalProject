import requests
from django.test import TestCase
from django.utils import timezone
from events.forms import EventForm
from events.models import Event
from django.contrib.auth.models import User


#API na mapy
try:
    response = requests.get("http://127.0.0.1:8000/api/events/upcoming/")
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")


#Tento test ověřuje datum zadání akce / nelze zadat nově akci co již byla

class EventFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_cannot_create_past_event(self):
        self.client.login(username='testuser', password='12345')
        form = EventForm(
            data={
                'title': 'Past Event',
                'start_date': timezone.now() - timezone.timedelta(days=1),
                'end_date': timezone.now(),
                'description': 'This is a past event.',
                'location': 'Test Location'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(Event.objects.count(), 0)

    def test_valid_form(self):
        data = {
            'title': 'Test Event',
            'start_date': timezone.now() + timezone.timedelta(days=1),
            'end_date': timezone.now() + timezone.timedelta(days=2),
            'description': 'This is a test description with more than 20 characters.',
            'location': 'Test Location'
        }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        data = {
            'title': '',
            'start_date': timezone.now() + timezone.timedelta(days=1),
            'end_date': timezone.now() + timezone.timedelta(days=2),
            'description': 'This is a test description with more than 20 characters.',
            'location': 'Test Location'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_short_description(self):
        data = {
            'title': 'Test Event',
            'start_date': timezone.now() + timezone.timedelta(days=1),
            'end_date': timezone.now() + timezone.timedelta(days=2),
            'description': 'Short desc.',
            'location': 'Test Location'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_start_date_in_past(self):
        data = {
            'title': 'Test Event',
            'start_date': timezone.now() - timezone.timedelta(days=1),
            'end_date': timezone.now() + timezone.timedelta(days=2),
            'description': 'This is a test description with more than 20 characters.',
            'location': 'Test Location'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_date', form.errors)

    def test_start_date_after_end_date(self):
        data = {
            'title': 'Test Event',
            'start_date': timezone.now() + timezone.timedelta(days=3),
            'end_date': timezone.now() + timezone.timedelta(days=2),
            'description': 'This is a test description with more than 20 characters.',
            'location': 'Test Location'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('Datum od nemůže být později než datum do.', form.errors['__all__'])

if __name__ == '__main__':
    import unittest
    unittest.main()