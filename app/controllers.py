from flask import url_for, redirect, request, render_template, session, flash, Response
from app import app, db


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/workshops')
def workshopsView():
	return render_template('workshops.html')

@app.route('/competitions')
def competitionsView():
	return render_template('competitions.html')

@app.route('/talks')
def talksView():
	return render_template('talks.html')

@app.route('/projects')
def projectsView():
	return render_template('will_be_updated.html')

@app.route('/sponsors')
def sponsorsView():
	return render_template('will_be_updated.html')

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
	return render_template('registration.html')

@app.route('/profile')
def profile():
	return render_template('userProfile.html')