# events/views.py
import json
import os
from typing import Optional, Dict, List, Any

import requests
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from dotenv import load_dotenv

load_dotenv() # for local testing

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://rekrutacja.teamwsuws.pl'

def list_events(request: HttpRequest) -> HttpResponse:
    headers = {'api-key': API_KEY}
    response = requests.get(f'{BASE_URL}/events/', headers=headers)

    events: List[Dict[str, Any]] = []
    if response.status_code == 200:
        events = response.json()

    return render(request, 'events/list_events.html', {'events': events})

def event_details(request: HttpRequest, event_id: int) -> HttpResponse:
    headers = {'api-key': API_KEY}
    response = requests.get(f'{BASE_URL}/events/{event_id}', headers=headers)

    if response.status_code == 200:
        event: Optional[Dict[str, Any]] = response.json()
    else:
        raise Http404("Event not found")

    return render(request, 'events/event_details.html', {'event': event})

def calendar_view(request: HttpRequest) -> HttpResponse:
    headers = {'api-key': API_KEY}
    response = requests.get(f'{BASE_URL}/events/', headers=headers)

    events: List[Dict[str, Any]] = []
    if response.status_code == 200:
        events = response.json()

    formatted_events: List[Dict[str, str]] = []
    for event in events:
        formatted_event: Dict[str, str] = {
            'title': event['name'],
            'start': event['start_time'],
            'url': reverse('event_details', args=[event['id']])
        }
        formatted_events.append(formatted_event)

    return render(request, 'events/calendar_view.html', {'events': json.dumps(formatted_events)})