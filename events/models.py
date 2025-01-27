from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', null=True)
    location = models.CharField(max_length=200, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creates_events', null=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    attendees = models.ManyToManyField(User, related_name='events', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

class Promotion(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='promotions/')
    description = models.TextField()

    def __str__(self):
        return self.title
