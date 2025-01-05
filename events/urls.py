# event_aggregator/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from events.views import home
from events import views

urlpatterns = [
    path('',home),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', include('registration.backends.default.urls')),
    path('add_event/', views.add_event, name='add_event'),
    path("events",views.event_list,name="event_list"),
    path('', views.home, name='home'),
]