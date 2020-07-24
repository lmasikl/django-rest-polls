import time
import datetime
import json

from django.urls import reverse


def test_polls_api(admin_api_client, poll_data):
    client = admin_api_client
    list_url = reverse('v1:poll-list')
    response = client.post(list_url, poll_data, format='json')
    assert response.status_code == 201, response.json()
    poll = response.data
    detail_url = reverse('v1:poll-detail', kwargs={'pk': poll['id']})
    response = client.get(detail_url)
    assert response.status_code == 200
    new_data = {'start_date': datetime.datetime.today().strftime('%Y-%m-%d')}
    response = client.patch(detail_url, new_data, format='json')
    assert response.status_code == 400, response.json()
    response = client.delete(detail_url)
    assert response.status_code == 204


def test_poll_questions_api(admin_api_client, questions_data):
    client = admin_api_client
    list_url = reverse('v1:question-list')
    text_question, choice_question, multiplechoice_question = questions_data
    response = client.post(list_url, text_question, format='json')
    assert response.status_code == 201, response.json()
    question = response.data
    assert len(question['choices']) == 1
    assert question['type'] == 'TEXT'
    detail_url = reverse('v1:question-detail', kwargs={'pk': question['id']})
    response = client.get(detail_url)
    assert response.status_code == 200
    response = client.patch(detail_url, choice_question, format='json')
    question = response.data
    assert response.status_code == 200
    assert len(question['choices']) == 2
    assert question['type'] == 'CHOICE'
    response = client.delete(detail_url)
    assert response.status_code == 204


def test_vote_on_poll_api(api_client, vote_data):
    vote_list_url = reverse('v1:vote-list')
    response = api_client.post(vote_list_url, data=vote_data, format='json')
    assert response.status_code == 201, response.json()

    response = api_client.get(vote_list_url, format='json')
    assert response.status_code == 200, response.json()
    assert len(response.data['results']) == 1

    response = api_client.get(f'{vote_list_url}?user=', format='json')
    assert response.status_code == 200, response.json()
    assert len(response.data['results']) == 1

    response = api_client.get(f'{vote_list_url}?user=1', format='json')
    assert response.status_code == 200, response.json()
    assert len(response.data['results']) == 0
