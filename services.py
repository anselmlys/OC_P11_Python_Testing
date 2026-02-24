from datetime import datetime


MAXIMUM_PLACES_PER_CLUB = 12


def is_future_competition(competition_date: str):
    competition_datetime = datetime.strptime(competition_date, '%Y-%m-%d %H:%M:%S')
    return competition_datetime > datetime.now()


def is_within_max_places_per_club(placesRequired: int):
    return placesRequired <= MAXIMUM_PLACES_PER_CLUB


def club_has_enough_points(club_points: str, placesRequired: int):
    return int(club_points) >= placesRequired
