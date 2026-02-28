import pytest
import json

import data_loader


def test_save_club_data(tmp_path):
    file_path = tmp_path / 'clubs.json'
    clubs = [{'name': 'Test Club', 'email': 'test@club.com', 'points': '10'},]

    data_loader.saveClubs(clubs, file_path)

    with open(file_path, 'r') as f:
        data = json.load(f)

    assert data == {'clubs': clubs}


def test_save_competitions_data(tmp_path):
    file_path = tmp_path / 'competitions.json'
    competitions = [
        {'name': 'Test Competition', 'date': '2026-02-12 12:30:00', 'numberOfPlaces': '15'},
        {'name': 'Test Competition 2', 'date': '2045-01-01 14:00:00', 'numberOfPlaces': '8'}
    ]

    data_loader.saveCompetitions(competitions, file_path)

    with open(file_path, 'r') as f:
        data = json.load(f)

    assert data == {'competitions': competitions}


def test_update_clubs_data(tmp_path):
    # Create and save clubs data in json file
    file_path = tmp_path / 'clubs.json'
    clubs_data = [
        {'name': 'Test Club', 'email': 'test@club.com', 'points': '10'},
        {'name': 'Test Club 2', 'email': 'test2@club.com', 'points': '8'}
    ]

    data_loader.saveClubs(clubs_data, file_path)

    # Load clubs data from new json file
    clubs = data_loader.loadClubs(file_path)

    # Define club to update and points to deduce
    club_to_update = clubs[0]
    places_required = 5

    # Update club points and rewrite the json file
    data_loader.updateClubPoints(clubs, club_to_update, places_required, file_path)

    expected_data = {'clubs':[
        {'name': 'Test Club', 'email': 'test@club.com', 'points': '5'},
        {'name': 'Test Club 2', 'email': 'test2@club.com', 'points': '8'}
    ]}

    # Retrieve data from updated json file
    with open(file_path, 'r') as f:
        data = json.load(f)

    assert expected_data == data


def test_update_competitions_data(tmp_path):
    # Create and save competitions data in json file
    file_path = tmp_path / 'competitions.json'
    competitions = [
        {'name': 'Test Competition', 'date': '2026-02-12 12:30:00', 'numberOfPlaces': '15'},
        {'name': 'Test Competition 2', 'date': '2045-01-01 14:00:00', 'numberOfPlaces': '8'}
    ]

    data_loader.saveCompetitions(competitions, file_path)

    # Retrieve competitions data from new json file
    competitions = data_loader.loadCompetitions(file_path)

    # Define the competition to modify and number of places to deduce
    competition_to_update = competitions[1]
    places_required = 5

    # Update and save new competition data in json file
    data_loader.updateCompetitionPlaces(competitions, competition_to_update,
                                        places_required, file_path)
    
    # Retrieve data from updated json file
    with open(file_path, 'r') as f:
        data = json.load(f)

    expected_data = {'competitions':[
        {'name': 'Test Competition', 'date': '2026-02-12 12:30:00', 'numberOfPlaces': '15'},
        {'name': 'Test Competition 2', 'date': '2045-01-01 14:00:00', 'numberOfPlaces': '3'}
    ]}

    assert data == expected_data
