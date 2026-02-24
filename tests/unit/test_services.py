import pytest

import services


def test_is_future_competition_returns_true():
    competition_date = '2045-03-27 10:00:00'
    future_competition = services.is_future_competition(competition_date)
    assert future_competition == True


def test_is_future_competition_returns_false():
    competition_date = '2000-03-27 10:00:00'
    future_competition = services.is_future_competition(competition_date)
    assert future_competition == False


def test_is_within_max_places_returns_true_when_under_limit():
    places_required = 12
    assert services.is_within_max_places_per_club(places_required) == True


def test_is_within_max_places_returns_false_when_over_limit():
    places_required = 13
    assert services.is_within_max_places_per_club(places_required) == False


def test_club_has_enough_points():
    club_points = '15'
    places_required = 5
    assert services.club_has_enough_points(club_points, places_required) == True


def test_club_does_not_have_enough_points():
    club_points = '15'
    places_required = 20
    assert services.club_has_enough_points(club_points, places_required) == False
