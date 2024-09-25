# tests/test_views

import pytest
from django.urls import reverse
from django.test import Client
from requests_mock import Mocker

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def mock_requests():
    with Mocker() as m:
        yield m

def test_list_events_view(client, mock_requests):
    url = 'https://rekrutacja.teamwsuws.pl/events/'
    mock_requests.get(url, json=[{'id': 1, 'name': 'Event 1'}], status_code=200)

    response = client.get(reverse('list_events'))

    assert response.status_code == 200
    assert 'events/list_events.html' in [t.name for t in response.templates]
    assert len(response.context['events']) == 1
    assert response.context['events'][0]['name'] == 'Event 1'

def test_event_details_view(client, mock_requests):
    event_id = 1
    url = f'https://rekrutacja.teamwsuws.pl/events/{event_id}'
    mock_requests.get(url, json={'id': event_id, 'name': 'Event 1'}, status_code=200)

    response = client.get(reverse('event_details', args=[event_id]))

    assert response.status_code == 200
    assert 'events/event_details.html' in [t.name for t in response.templates]
    assert response.context['event']['name'] == 'Event 1'

def test_event_details_view_404(client, mock_requests):
    event_id = 999
    url = f'https://rekrutacja.teamwsuws.pl/events/{event_id}'
    mock_requests.get(url, status_code=404)

    response = client.get(reverse('event_details', args=[event_id]))

    assert response.status_code == 404