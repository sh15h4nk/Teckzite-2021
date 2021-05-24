from app.models import *
import requests
from creds import GOOGLE_DISCOVERY_URL

def getEvents(eventId='all'):
	if eventId == 'all':
		events = Event.query.all()
		return events

	event = Event.query.filter_by(eventId=eventId).first()
	return event



def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
