import pytest
import html

import server


@pytest.fixture
def app():
    server.app.config.update(
        TESTING=True,
    )
    return server.app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def clubs_sample():
    return [{'name': 'Test Club', 'email': 'test@club.com', 'points': '10'}]


@pytest.fixture
def competitions_sample():
    return [
        {'name': 'Test Competition', 'date': '2026-02-12 12:30:00', 'numberOfPlaces': '15'},
        {'name': 'Test Competition 2', 'date': '2045-01-01 14:00:00', 'numberOfPlaces': '8'}
    ]


@pytest.fixture
def patch_data(monkeypatch, clubs_sample, competitions_sample):
    monkeypatch.setattr(server, 'clubs', clubs_sample)
    monkeypatch.setattr(server, 'competitions', competitions_sample)
    return clubs_sample, competitions_sample


def test_show_summary_valid_email(client, patch_data):
    response = client.post(
        '/showSummary',
        data={'email': 'test@club.com'}
    )

    assert response.status_code == 200
    # Check that the email appears correctly on the page
    assert b'test@club.com' in response.data
    # Verify an element of the welcome template to check if it is displayed properly
    assert b'Points available:' in response.data


def test_show_summary_invalid_email(client, patch_data):
    response = client.post(
        '/showSummary',
        data={'email': 'unknown@club.com'},
        follow_redirects=True
    )

    page = html.unescape(response.data.decode('utf-8'))

    assert response.status_code == 200
    # Verify that the user is redirected to 'index'
    assert 'Please enter your secretary email to continue:' in page
    # Check that the flash message appears
    assert 'Sorry, that email wasn\'t found.' in page


def test_purchase_places_with_enough_points(client, patch_data):
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Test Competition',
            'club': 'Test Club',
            'places': '5',
        }
    )

    assert response.status_code == 200
    # Verify if flash message appear
    assert b'Great-booking complete!' in response.data
    # Verify an element of the welcome template to check if it is displayed properly
    assert b'Points available:' in response.data
    # Check that the available competition places have been updated
    assert server.competitions[0]['numberOfPlaces'] == 10
    # Check that the points used have been deducted from the club's total
    assert server.clubs[0]['points'] == 5


def test_purchase_places_without_enough_points(client, patch_data):
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Test Competition',
            'club': 'Test Club',
            'places': '11',
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    # Verify if flash message appear
    assert b'You do not have enough points.' in response.data
    # Verify an element of the booking template to check if it is displayed properly
    assert b'How many places?' in response.data
    # Check that the number of places available for the competition has not changed
    assert server.competitions[0]['numberOfPlaces'] == '15'
    # Check that the club's points have not changed
    assert server.clubs[0]['points'] == '10'


def test_purchase_more_than_12_places(client, patch_data):
    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Test Competition',
            'club': 'Test Club',
            'places': '13',
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    # Verify an element of the booking template to check if it is displayed properly
    assert b'How many places?' in response.data
    # Verify if flash message appear
    assert b'You cannot book more than 12 places.' in response.data
    # Check that the number of places available for the competition has not changed
    assert server.competitions[0]['numberOfPlaces'] == '15'
    # Check that the club's points have not changed
    assert server.clubs[0]['points'] == '10'
