import os
import creds
import pymysql


DEGUG = True


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(creds.dbuser, creds.dbpasswd, creds.dbhost, creds.dbname)
SQLALCHEMY_DATABASE_URI = conn


# SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')

SESSION_TYPE = 'sqlalchemy'
SQLALCHEMY_TRACK_MODIFICATIONS = False

THREADS_PER_PAGE = 2


SECRET_KEY = creds.secret_key


S3_BUCKET                 = "tzimageupload"
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)


MAIL_SERVER = creds.mail_server
MAIL_PORT = creds.mail_port
MAIL_USE_TLS = True
MAIL_USERNAME = creds.email_username
MAIL_PASSWORD = creds.email_passwd