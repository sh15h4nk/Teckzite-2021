from flask import url_for, redirect, request, render_template, session, flash, Response, escape, Markup, session
from app import app, db
from app.models import TechUser
from app.functions import *
from creds import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# #oauth
# from flask_login import (
# 	LoginManager,
#     current_user,
#     login_required,
#     login_user,
#     logout_user,
# )

# from oauthlib.oauth2 import WebApplicationClient
# import requests, json

# client = WebApplicationClient(GOOGLE_CLIENT_ID)



# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return TechUser.query.get(user_id)

# @login_manager.unauthorized_handler
# def unauthorized():
#     flash("You must login ")
#     return redirect(url_for('index'))



# @app.route('/')
# def temp():
# 	if 'id' in session:
# 		return ("You are authenticaed")
# 	else:
# 		return ("You are not authenticaed")



# @app.route("/login", methods=['GET', 'POST'])
# def login():
 
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]

#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)


# @app.route("/login/callback")
# def callback():

# 	code = request.args.get("code")

# 	google_provider_cfg = get_google_provider_cfg()
# 	token_endpoint = google_provider_cfg["token_endpoint"]

# 	token_url, headers, body = client.prepare_token_request(
# 		token_endpoint,
# 		authorization_response=request.url,
# 		redirect_url=request.base_url,
# 		code=code
# 	)
# 	token_response = requests.post(
# 		token_url,
# 		headers=headers,
# 		data=body,
# 		auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
# 	)

# 	client.parse_request_body_response(json.dumps(token_response.json()))

# 	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
# 	uri, headers, body = client.add_token(userinfo_endpoint)
# 	userinfo_response = requests.get(uri, headers=headers, data=body)

# 	if userinfo_response.json().get("email_verified"):
# 	    unique_id = userinfo_response.json()["sub"]
# 	    users_email = userinfo_response.json()["email"]
# 	    picture = userinfo_response.json()["picture"]
# 	    users_name = userinfo_response.json()["given_name"]
# 	else:
# 	    return "User email not available or not verified by Google.", 400


# 	user = TechUser.query.filter_by(userId=unique_id).first()

# 	if not user:
# 		new_user = TechUser(userId=unique_id, name=users_name, email=users_email)
# 		db.session.add(new_user)
# 		db.session.commit()
	    
# 	session['id'] = 1

# 	# if not user.registration_status:
# 	# 	return redirect(url_for('register'))

# 	return redirect(url_for("temp"))


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

	print(markup['structure'])

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

@app.route('/register')
def register():
	return render_template('registration.html')

@app.route('/profile')
def profile():
	return render_template('userProfile.html')
