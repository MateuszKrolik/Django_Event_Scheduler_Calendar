# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_events, name='list_events'),
    path('<int:event_id>/', views.event_details, name='event_details'),
]