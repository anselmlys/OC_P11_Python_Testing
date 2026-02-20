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


def test_show_summary_valid_email(client, monkeypatch):
    monkeypatch.setattr(server, 'clubs', [
        {'name': 'Test Club', 'email': 'test@club.com', 'points': '10'}
    ])
    monkeypatch.setattr(server, 'competitions', [
        {'name': 'Test Competition', 'date': '2026-02-12 12:30:00', 'numberOfPlaces': '15'}
    ])

    response = client.post(
        '/showSummary',
        data={'email': 'test@club.com'}
    )

    assert response.status_code == 200
    assert b'test@club.com' in response.data
    assert b'Test Competition' in response.data


def test_show_summary_invalid_email(client, monkeypatch):
    monkeypatch.setattr(server, 'clubs', [
        {'name': 'Test Club', 'email': 'test@club.com', 'points': '10'}
    ])

    response = client.post(
        '/showSummary',
        data={'email': 'unknown@club.com'},
        follow_redirects=True
    )

    page = html.unescape(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'Please enter your secretary email to continue:' in page
    assert 'Sorry, that email wasn\'t found.' in page
