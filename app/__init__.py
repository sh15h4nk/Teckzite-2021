from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SESSION_SQLALCHEMY'] = db

from app.controllers import *

if __name__ == '__main__':
	app.run('0.0.0.0', port = 7331)
