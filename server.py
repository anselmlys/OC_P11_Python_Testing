from flask import Flask, render_template, request, redirect, flash, url_for

from data_loader import (loadClubs, loadCompetitions, updateClubPoints,
                         updateCompetitionPlaces, CLUBS_FILEPATH, COMPETITIONS_FILEPATH)
from services import (is_bookable, is_within_max_places_per_club,
                      club_has_enough_points, has_enough_available_places)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions(COMPETITIONS_FILEPATH)
clubs = loadClubs(CLUBS_FILEPATH)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = next((club for club in clubs if club['email'] == request.form['email']), None)

    if club is None:
        flash('Sorry, that email wasn\'t found.')
        return redirect(url_for('index'))

    else:
        competitions_view = [
            {**comp, 'is_bookable': is_bookable(comp)}
            for comp in competitions
        ]
        return render_template('welcome.html', club=club, competitions=competitions_view)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash('Something went wrong-please try again')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if not is_within_max_places_per_club(placesRequired):
        flash('You cannot book more than 12 places.')
        return redirect(url_for('book', club=club['name'], competition=competition['name']))
    elif not has_enough_available_places(competition['numberOfPlaces'], placesRequired):
        flash('You cannot book more than the number of available places.')
        return redirect(url_for('book', club=club['name'], competition=competition['name']))
    elif not club_has_enough_points(club['points'], placesRequired):
        flash('You do not have enough points.')
        return redirect(url_for('book', club=club['name'], competition=competition['name']))
    else:
        updateCompetitionPlaces(competitions, competition, placesRequired, COMPETITIONS_FILEPATH)
        updateClubPoints(clubs, club, placesRequired, CLUBS_FILEPATH)
        flash('Great-booking complete!')
        competitions_view = [
            {**comp, 'is_bookable': is_bookable(comp)}
            for comp in competitions
        ]
        return render_template('welcome.html', club=club, competitions=competitions_view)


@app.route('/clubPoints')
def displayClubPoints():
    return render_template('club_points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
