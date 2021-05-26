from app.models import *
import requests
from creds import GOOGLE_DISCOVERY_URL

def getEvents(eventId='all'):
	if eventId == 'all':
		events = Event.query.filter_by(hidden=0).all()
		return events

	event = Event.query.filter_by(hidden=0, eventId=eventId).first()
	return event

def addAddress(t_userId, address_data):
	address = Address(address_data)
	address.t_userId = t_userId
	db.session.add(address)
	db.session.commit()

	return address

def addUser(userId, data):
	del data['state']
	del data['country']
	del data['city']

	user = TechUser.query.filter_by(userId=userId).first()
	if not user:
		return

	user.update(data)
	db.session.commit()

	return user

def addRguktUser(userId, data):
	
	user = TechUser.query.filter_by(userId=userId).first()
	if not user:
		return

	user.update(data)
	db.session.commit()

	return user


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


