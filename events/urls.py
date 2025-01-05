from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),  # cesta pro seznam událostí
    path('<int:id>/', views.event_detail, name='event_detail'),  # cesta pro detail události
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
]


