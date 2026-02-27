import pytest

import services


# Test the function is_future_competition

def test_is_future_competition_returns_true():
    competition_date = '2045-03-27 10:00:00'
    future_competition = services.is_future_competition(competition_date)
    assert future_competition == True


def test_is_future_competition_returns_false():
    competition_date = '2000-03-27 10:00:00'
    future_competition = services.is_future_competition(competition_date)
    assert future_competition == False


# Test the function is_not_full

def test_is_not_full_returns_true_when_places_available():
    competition_places = '5'
    assert services.is_not_full(competition_places) == True


def test_is_not_full_returns_false_when_no_place_left():
    competition_places = '0'
    assert services.is_not_full(competition_places) == False


# Test the function is_bookable

def test_competition_is_bookable():
    competition = {
        'name': 'Test Competition',
        'date': '2045-02-12 12:30:00',
        'numberOfPlaces': '15'
    }
    assert services.is_bookable(competition) == True


def test_is_bookable_returns_false_when_date_has_passed():
    competition = {
        'date': '2000-02-12 12:30:00',
        'numberOfPlaces': '15'
    }
    assert services.is_bookable(competition) == False


def test_is_bookable_returns_false_when_competition_is_full():
    competition = {
        'date': '2045-02-12 12:30:00',
        'numberOfPlaces': '0'
    }
    assert services.is_bookable(competition) == False


# Test the function is_within_max_places_per_club

def test_is_within_max_places_returns_true_when_under_limit():
    places_required = 12
    assert services.is_within_max_places_per_club(places_required) == True


def test_is_within_max_places_returns_false_when_over_limit():
    places_required = 13
    assert services.is_within_max_places_per_club(places_required) == False


# Test the function club_has_enough_points

def test_club_has_enough_points():
    club_points = '15'
    places_required = 5
    assert services.club_has_enough_points(club_points, places_required) == True


def test_club_does_not_have_enough_points():
    club_points = '15'
    places_required = 20
    assert services.club_has_enough_points(club_points, places_required) == False
