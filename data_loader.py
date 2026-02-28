import json


CLUBS_FILEPATH = 'clubs.json'
COMPETITIONS_FILEPATH = 'competitions.json'


def loadClubs(path: str) -> list:
    with open(path) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions(path: str) -> list:
    with open(path) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def saveClubs(clubs: list, path: str):
    clubs_data = {'clubs': clubs}
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(clubs_data, file, indent=2, ensure_ascii=False)


def saveCompetitions(competitions: list, path: str):
    competitions_data = {'competitions': competitions}
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(competitions_data, file, indent=2, ensure_ascii=False)


def updateClubPoints(clubs: list, club_to_update: dict,
                     places_required: int, file_path: str):
    # Deduct points used for the booking
    new_points = int(club_to_update['points']) - places_required
    club_to_update['points'] = str(new_points)

    # Rewrite json with updated data
    saveClubs(clubs, file_path)


def updateCompetitionPlaces(competitions: list, competition_to_update: dict,
                            places_required: int, file_path: str):
    # Deduct places required for the booking
    new_number_of_places = int(competition_to_update['numberOfPlaces']) - places_required
    competition_to_update['numberOfPlaces'] = str(new_number_of_places)

    # Rewrite json with updated data
    saveCompetitions(competitions, file_path)
