# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('<int:event_id>/', views.event_details, name='event_details'),
    path('events-list/', views.list_events, name='list_events'),

]