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

def addAddress(t_userId, address_data):
	address = Address(address_data['state'], address_data['district'], address_data['city'], address_data['pin'])
	address.t_userId = t_userId
	db.session.add(address)
	db.session.commit()
	return address

def addUser(userId, data, idcard_url=""):

	user = TechUser.query.filter_by(phone=data['phone']).first()
	if user:
		return "Phone number already exists!"

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
	user.update({'registration_status': 1})
	db.session.commit()

	return user.first()

def addCA(name, email, phone, gender, college, collegeId, year, branch):
	ca_id = generate_ca_id()

	new_ca = CA(ca_id, name, email, phone, gender, college, collegeId, year, branch)

	return ca


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
	pattern = r'(^[a-zA-Z0-9]{7})@rgukt[a-z]*.ac.in$'
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
    
    return current_ca_id


def registration_required(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if not current_user.registration_status:
			flash("Please add your details")
			return redirect(url_for('register'))
		else:
			return func(*args, **kwargs)
	return decorated_function


def sendMail(user, message_title, template):
	msg = Message(message_title, sender='no-reply@teckzite.org', recipients=[user.email])
	msg.html = render_template(template)
	mail.send(msg)