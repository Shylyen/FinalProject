"""
URL configuration for event_aggregator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path

"""
from django.contrib import admin
from django.urls import path, include
from events import views
from django.contrib.auth import views as auth_views

from events.views import user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name='home'),  # Domovská stránka
    path('events/', include('events.urls')),  # Události
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/register/', include('registration.backends.default.urls')),
    path('add/', views.add_event, name='add_event'),
    path('search/', views.search_results, name='search_results'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('', views.event_list, name='event_list'),  # Existing view
    path('api-events/', views.api_event_list, name='api_event_list'),  # New API consumer view
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('about/', views.about, name='about'),
    path('api/', include('events.urls')),
]