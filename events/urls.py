
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.event_list, name='event_list'),  # cesta pro event_list
    path('event/<int:event_id>/attend/', views.attend_event, name='attend_event'),  # Přihlášení na událost
    path('event/<int:event_id>/unattend/', views.unattend_event, name='unattend_event'),  # Odhlašování z události
]



