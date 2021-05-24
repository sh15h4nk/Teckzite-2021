from app.models import *

def getEvents(eventId='all'):
	if eventId == 'all':
		events = Event.query.all()
		return events

	event = Event.query.filter_by(eventId=eventId).first()
	return event


