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
from django.conf import settings  # Přidáno pro import settings
from django.conf.urls.static import static  # Přidáno pro statické soubory

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name='home'),  # Domovská stránka
    path('events/', include('events.urls')),  # Události
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('accounts/register/', include('registration.backends.default.urls')),
    path('add/', views.add_event, name='add_event'),
    path('search/', views.search_results, name='search_results'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # Detail události
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),  # Úprava události
    path('api-events/', views.api_event_list, name='api_event_list'),  # API pro události
    path('about/', views.about, name='about'),
    path('api/', include('events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

