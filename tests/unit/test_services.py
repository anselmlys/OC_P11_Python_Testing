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
