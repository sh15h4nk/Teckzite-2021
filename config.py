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
