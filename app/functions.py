from app.models import *
import requests
from creds import GOOGLE_DISCOVERY_URL
from flask_login import current_user
from flask import redirect, url_for

def getEvents(eventId='all'):
	if eventId == 'all':
		events = Event.query.filter_by(hidden=0).all()
		return events

	event = Event.query.filter_by(hidden=0, eventId=eventId).first()
	return event

def addAddress(t_userId, address_data):
	address = Address(address_data['state'], address_data['district'], address_data['city'])
	address.t_userId = t_userId
	db.session.add(address)
	db.session.commit()
	return address

def addUser(userId, data):

	del data['state']
	del data['district']
	del data['city']

	user = TechUser.query.filter_by(userId=userId).first()
	if not user:
		return

	user.update(data)
	user.update({'registration_status': 1})
	db.session.commit()

	return user

def addRguktUser(userId, data):
	
	user = TechUser.query.filter_by(userId=userId).first()
	if not user:
		return

	user.update(data)
	user.update({'registration_status': 1})
	db.session.commit()

	return user


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def reg_stat(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if current_user.is_authenticated and not current_user.registration_status:
			return redirect(url_for('register'))
		else:
			return func(*args, **kwargs)
	return decorated_function

def registration_stat():
	if current_user.is_authenticated and not current_user.registration_status:
		return redirect(url_for('register'))