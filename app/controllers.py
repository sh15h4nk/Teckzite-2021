from flask import url_for, redirect, request, render_template, session, flash, Response, escape, Markup
from app import app, db
from app.functions import *

def dict_escape(d):
	for k,v in d.items():
		d[k] = Markup(d[k]).unescape()

		return d

@app.route('/')
def temp():
	return Response()

@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/workshops')
def workshopsView():
	return render_template('updating.html')

@app.route('/competitions')
def competitionsView():

	events = getEvents()
	return render_template('competitions.html', events = events)

@app.route('/event-details/<eventId>')
def eventDetailsView(eventId):

	
	event = getEvents(eventId)

	markup = {}
	markup['description'] = Markup(event.description).unescape()
	markup['structure'] = Markup(event.structure).unescape()
	markup['timeline'] = Markup(event.timeline).unescape()
	markup['rules'] = Markup(event.rules).unescape()


	return render_template('event-details.html', event=event, markup=markup)

@app.route('/talks')
def talksView():
	return render_template('updating.html')

@app.route('/projects')
def projectsView():
	return render_template('updating.html')

@app.route('/sponsors')
def sponsorsView():
	return render_template('updating.html')

@app.route('/about')
def aboutView():
	return render_template('about.html')

@app.route('/team')
def teamView():
	return render_template('team.html')

@app.route('/devTeam')
def devteamView():
	return render_template('web_team.html')

@app.route('/register')
def register():
	return render_template('updating.html')

@app.route('/profile')
def profile():
	return render_template('updating.html')