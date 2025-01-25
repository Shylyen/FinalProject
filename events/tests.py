import requests
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
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
        url = reverse('add')
        data = {
            'title': 'Past Event',
            'start_date': timezone.now() - timezone.timedelta(days=1),
            'end_date': timezone.now(),
            'description': 'This is a past event.',
            'location': 'Test Location'
        }
        response = self.client.post(url, data)
        self.assertFormError(response, 'form', 'start_date', 'Datum od nemůže být v minulosti.')


        self.assertEqual(Event.objects.count(), 0)
