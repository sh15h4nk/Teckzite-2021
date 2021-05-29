from app.models import *
import requests
from creds import GOOGLE_DISCOVERY_URL
from flask_login import current_user
from flask import redirect, url_for
from functools import wraps
from flask import flash
import re



def getEvents(eventId='all'):
	if eventId == 'all':
		events = Event.query.filter_by(hidden=0).all()
		return events

	event = Event.query.filter_by(hidden=0, eventId=eventId).first()
	return event

def addAddress(t_userId, address_data):
	address = Address(address_data['state'], address_data['district'], address_data['city'], address_data['pin'])
	address.t_userId = t_userId
	db.session.add(address)
	db.session.commit()
	return address

def addUser(userId, data):

	del data['state']
	del data['district']
	del data['city']
	del data['pin']

	user = TechUser.query.filter_by(userId=userId)
	if not user:
		return

	user.update(data)
	user.update({'registration_status': 1})
	db.session.commit()

	return user.first()

def addRguktUser(userId, data):
	
	user = TechUser.query.filter_by(userId=userId)
	if not user:
		return

	user.update(data)
	user.update({'registration_status': 1})
	db.session.commit()

	return user.first()


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def is_rguktn(email):
	pattern = r'[n|N][\d]{6}@rguktn.ac.in'
	return re.match(pattern, email)


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


def registration_required(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if not current_user.registration_status:
			flash("Please add your details")
			return redirect(url_for('register'))
		else:
			return func(*args, **kwargs)
	return decorated_function

