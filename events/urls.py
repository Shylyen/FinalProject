from django.template.context_processors import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from event_aggregator import settings
from . import views
from .views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.event_list, name='event_list'),  # cesta pro event_list
]





