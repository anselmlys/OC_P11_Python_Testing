from datetime import datetime


MAXIMUM_PLACES_PER_CLUB = 12


def is_future_competition(competition_date: str) -> bool:
    competition_datetime = datetime.strptime(competition_date, '%Y-%m-%d %H:%M:%S')
    return competition_datetime > datetime.now()


def is_not_full(competition_places: str) -> bool:
    return int(competition_places) > 0


def is_bookable(competition: dict) -> bool:
    return is_future_competition(competition['date']) and is_not_full(competition['numberOfPlaces'])


def is_within_max_places_per_club(placesRequired: int) -> bool:
    return placesRequired <= MAXIMUM_PLACES_PER_CLUB


def club_has_enough_points(club_points: str, placesRequired: int) -> bool:
    return int(club_points) >= placesRequired


def has_enough_available_places(competition_places: str, places_required: str) -> bool:
    return int(competition_places) >= int(places_required)
