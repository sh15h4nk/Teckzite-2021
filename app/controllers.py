from flask import url_for, redirect, request, render_template, flash, Response, escape, Markup
from app import app, db
from app.models import TechUser
from app.functions import *
from creds import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

#oauth
from flask_login import (
	LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
import requests, json

client = WebApplicationClient(GOOGLE_CLIENT_ID)



login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return TechUser.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash("You are not authorised")
    return redirect('index')


@app.route('/robots.txt')
def noindex():
	r = Response(response="User-Agent: Googlebot\nAllow: /\n\nUser-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
	r.headers["Content-Type"] = "text/plain; charset=utf-8"
	return r



@app.route("/login", methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		if not current_user.registration_status:

			if current_user.email.endswith("rguktn.ac.in"):
				return redirect(url_for('registerRgukt'))
			else:
				return redirect(url_for('registerUser'))

		else:
			flash("Already logged in")
			return redirect(url_for('index'))

	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg["authorization_endpoint"]

	request_uri = client.prepare_request_uri(authorization_endpoint,redirect_uri=request.base_url + "/callback",scope=["openid", "email", "profile"])
	return redirect(request_uri)


@app.route("/login/callback")
def callback():

	code = request.args.get("code")

	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]

	token_url, headers, body = client.prepare_token_request(
		token_endpoint,
		authorization_response=request.url,
		redirect_url=request.base_url,
		code=code
	)
	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
	)

	client.parse_request_body_response(json.dumps(token_response.json()))

	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	uri, headers, body = client.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)

	if userinfo_response.json().get("email_verified"):
	    unique_id = userinfo_response.json()["sub"]
	    users_email = userinfo_response.json()["email"]
	    picture = userinfo_response.json()["picture"]
	    users_name = userinfo_response.json()["given_name"]
	else:
	    return "User email not available or not verified by Google.", 400


	user = TechUser.query.filter_by(userId=unique_id).first()

	# if user logins first time with this email, add user to the database and then login the user
	if not user:
		new_user = TechUser(userId=unique_id, name=users_name, email=users_email)
		db.session.add(new_user)
		db.session.commit()

		login_user(new_user)
		flash("Logged in successfully")
		

	# if user is already logged in with this email, just login the user
	else:
		login_user(user)
		flash("Logged in successfully")
	    

	# check if user registration is complete
	if not current_user.registration_status:

		if current_user.email.endswith("rguktn.ac.in"):
			return redirect(url_for('registerRgukt'))
		else:
			return redirect(url_for('registerUser'))


	return redirect(url_for("index"))

@app.route('/logout')
def logout():
	logout_user()
	flash("You have been logged out")
	return redirect(url_for('index'))



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/workshops')
def workshopsView():
	return render_template('workshops.html')

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

	# print(markup['structure'])

	return render_template('event-details.html', event=event, markup=markup)

@app.route('/talks')
def talksView():
	return render_template('talks.html')

@app.route('/summits')
def summitsView():
	return render_template('updating.html')

@app.route('/virtual-exibition')
def virtualView():
	return render_template('updating.html')



@app.route('/project-expo')
def projectsView():
	return render_template('project-expo.html')

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

@app.route('/register.rgukt', methods=['GET', 'POST'])
@login_required
def registerRgukt():

	if request.method == 'POST':
		
		try:
			user = addRguktUser(current_user.userId, request.form)
			flash("Your details have been added successfully")
			return redirect(url_for('index'))

		except Exception as e:
			raise e


	return render_template('register_rgukt.html')


@app.route('/register.user', methods=['GET', 'POST'])
@login_required
def registerUser():

	if request.method == 'POST':
		
		address_data = {}
		address_data['state'] = request.form['state']
		address_data['district'] = request.form['district']
		address_data['city'] = request.form['city']

		user_data = dict(request.form)

		try:
			user = addUser(current_user.userId, user_data)
			address = addAddress(user.userId, address_data)
			flash("Your details have been added successfully")
			return redirect(url_for('index'))

		except Exception as e:
			raise e



	return render_template('register_user.html')


@app.route('/profile')
def profile():
	return render_template('userProfile.html')
