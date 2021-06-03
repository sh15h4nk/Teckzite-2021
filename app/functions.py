from app.models import *
import requests
from creds import GOOGLE_DISCOVERY_URL
from flask_login import current_user
from flask import redirect, url_for, render_template
from functools import wraps
from flask import flash
from app import mail
import re, boto3, botocore, uuid
from config import *
from flask_mail import Message 


s3 = boto3.resource("s3")


def getEvents(eventId='all'):
	if eventId == 'all':
		events = Event.query.filter_by(hidden=0).all()
		return events

	event = Event.query.filter_by(hidden=0, eventId=eventId).first()
	return event

def getWorkshops(workshopId='all'):
	if workshopId == 'all':
		workshops = Workshop.query.filter_by(hidden=0).all()
		return workshops

	workshop = Workshop.query.filter_by(hidden=0, workshopId=workshopId).first()
	return workshop


def addAddress(t_userId, address_data):
	address = Address(address_data['state'], address_data['district'], address_data['city'], address_data['pin'])
	address.t_userId = t_userId
	db.session.add(address)
	db.session.commit()
	return address

def addUser(userId, data, idcard_url=""):

	user = TechUser.query.filter_by(userId=userId)
	if not user:
		return

	if idcard_url:
		data['idcard_url'] = idcard_url

	user.update(data)
	user.update({'registration_status': 1})
	db.session.commit()

	return user.first()

def addRguktUser(userId, data):

	user = TechUser.query.filter_by(phone=data['phone']).first()
	if user:
		return "Phone number already exists!"
	
	user = TechUser.query.filter_by(userId=userId)
	if not user:
		return

	user.update(data)
	user.update({'college': 'RGUKT-N'})
	user.update({'registration_status': 1})
	db.session.commit()

	return user.first()

def addCA(name, email, phone, gender, college, collegeId, year, branch):
	ca_id = generate_ca_id()

	new_ca = CA(ca_id, name, email, phone, gender, college, collegeId, year, branch)
	db.session.add(new_ca)
	db.session.commit()

	return new_ca


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def is_rguktn(email):
	pattern = r'[n|N][\d]{6}@rguktn.ac.in'
	return re.match(pattern, email)

def is_rgukt(email):
	return email.endswith('@rguktn.ac.in') or email.endswith('@rguktrkv.ac.in') or email.endswith('@rguktong.ac.in') or email.endswith('@rguktsklm.ac.in') or email.endswith('@rgukt.ac.in')

def get_college(email):
	pattern = r'rgukt([a-z]*).ac.in$'
	clg_suffix = re.findall(pattern, email)[0]
	return "RGUKT-"+clg_suffix.upper()

def get_college_id(email):
	pattern = r'(^[a-zA-Z0-9]+)@rgukt[a-z]*.ac.in$'
	Id = re.findall(pattern, email)[0]
	return Id.upper()



def upload_file_to_s3(file, filename, file_ext, acl="public-read"):

    bucket = s3.Bucket(S3_BUCKET)
    obj = bucket.Object(f"{filename}.{file_ext}")
    obj.upload_fileobj(
        file,
        ExtraArgs={
            "ACL": acl,
            "ContentType": f"image/{file_ext}"
        }
    )
    return "{}{}.{}".format(S3_LOCATION, filename, file_ext)


def generate_techzite_id():

    currentId = CurrentId.query.first()
    current_techzite_id = currentId.current_techzite_id
    
    currentId.current_techzite_id += 1
    db.session.commit()
    
    return "TZ"+str(current_techzite_id)

def generate_event_id():

    currentId = CurrentId.query.first()
    current_event_id = currentId.current_event_id
    
    currentId.current_event_id += 1
    db.session.commit()

    return "EV"+str(current_event_id)

def generate_workshop_id():

    currentId = CurrentId.query.first()
    current_workshop_id = currentId.current_workshop_id
    
    currentId.current_workshop_id += 1
    db.session.commit()

    return "WS"+str(current_workshop_id)


def generate_ca_id():

    currentId = CurrentId.query.first()
    current_ca_id = currentId.current_ca_id
    
    currentId.current_ca_id += 1
    db.session.commit()
    
    return "CA" + str(current_ca_id)


def generate_team_id():

    currentId = CurrentId.query.first()
    current_team_id = currentId.current_team_id
    
    currentId.current_team_id += 1
    db.session.commit()
    
    return "TM" + str(current_team_id)


def registration_required(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if not current_user.registration_status:
			flash("Please add your details")
			return redirect(url_for('register'))
		else:
			return func(*args, **kwargs)
	return decorated_function


def sendMail(user, message_title, template, mesg):
	msg = Message(message_title, sender='no-reply@teckzite.org', recipients=[user.email])
	msg.html = render_template(template, msg=mesg)
	mail.send(msg)


# events and teams


def create_team(team_members, eventId):
	teamId = generate_team_id()
	new_team = Team(teamId, eventId)
	db.session.add(new_team)
	db.session.commit()

	return teamId

def add_team_members(team_members, teamId):

	team = Team.query.filter_by(teamId=teamId)
	for userId in team_members:
		new_member = Member(teamId, userId)
		db.session.add(new_member)

		send_team_request(userId, teamId)

	db.session.commit()


def is_complete_team():
	return

def send_team_request(userId, teamId):
	team = Team.query.filter_by(teamId = teamId).first()
	eventId = team.event_id

	tech_user = TechUser.query.filter_by(userId=userId)
	new_team_request = TeamRequest(teamId)
	db.session.add(new_team_request)
	db.session.commit()



def accept_team_request(teamId, userId):
	member = Member.query.filter_by(teamId=teamId, userId=userId)
	member.update({'stauts': 1})
	db.session.commit()

	team_request = TeamRequest.query.filter_by(team_id=teamId, user_id=userId)
	db.session.delete(team_request)
	db.session.commit()


def decline_team_request(teamId, userId):
	team_request = TeamRequest.query.filter_by(team_id=teamId, user_id=userId)
	db.session.delete(team_request)
	db.session.commit()


def modify_member_status(teamId, userId, action):
	member = Member.query.filter_by(teamId=teamId, userId=userId)
	member.update({'stauts': action})
	db.session.commit()

def update_team_status(teamId):
	team = Team.query.filter_by(teamId=teamId).first()
	for member in team.members:
		if member.stauts == 0:
			return False
	else:
		Team.query.filter_by(teamId=teamId).update({'team_status': 1})
		return True


def get_max_members(eventId):
	event = Event.query.filter_by(eventId=eventId).first()
	return event.max_teamsize

def get_min_members(eventId):
	event = Event.query.filter_by(eventId=eventId).first()
	return event.min_teamsize


def are_valid_members(team_members):
	for member in team_members:
		user = TechUser.query.filter_by(userId=member).first()
		if not user:
			return False
	else:
		return True

def is_valid_team_request(team_members, eventId):
	event = Event.query.first_by(eventId=eventId).first()
	

	for team in event.teams:
		for member in team.members:
			if member.user_id in team_members and member.status == 1:
				return False
	else:
		return True 

def is_valid_team(teamId):
	team = Team.query.filter_by(teamId=teamId).first()
	if not team:
		return False
	return True

def get_my_events(userId):
	events = []
	members = Members.query.filter_by(user_id = userId).all()
	for member in members:
		team = Team.query.filter_by(teamId = member.team_id, team_status=1).first()
		event = Event.query.filter_by(eventId=team.event_id).first()
		events.append(event)

	return events

def get_my_teams(userId):
	teams = []
	members = Members.query.filter_by(user_id = userId).all()
	for member in members:
		team = Team.query.filter_by(teamId = member.team_id, team_status=1).first()
		teams.append(team)

	return teams



