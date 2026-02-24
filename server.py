import json
from flask import Flask, render_template, request, redirect, flash, url_for

from services import is_future_competition


MAXIMUM_PLACES_PER_CLUB = 12


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = next((club for club in clubs if club['email'] == request.form['email']), None)

    if club is None:
        flash('Sorry, that email wasn\'t found.')
        return redirect(url_for('index'))

    else:
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    future_competition = is_future_competition(competition_date=foundCompetition['date'])
    if foundClub and foundCompetition and future_competition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    elif not future_competition:
        flash('You can no longer register to this competition.')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('Something went wrong-please try again')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > MAXIMUM_PLACES_PER_CLUB:
        flash('You cannot book more than 12 places.')
        return render_template('booking.html', club=club, competition=competition)
    elif placesRequired > int(club['points']):
        flash('You do not have enough points.')
        return render_template('booking.html', club=club, competition=competition)
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))