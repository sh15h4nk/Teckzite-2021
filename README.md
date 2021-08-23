# Teckzite-2021

Website at teckzite.org, an annual national level tech fest, organized by [SDCAC](https://intranet.rguktn.ac.in/sdcac/) from [RGUKT Nuzvid](https://rguktn.ac.in/) across the country.

## Requirements
- linux system
- Python 3
- MySQL database
- Google Oauth


## OAuth Config

To run the server locally, follow below steps:

- `export FLASK_APP=run`
- `export FLASK_ENV=development`
- `export OAUTHLIB_INSECURE_TRANSPORT=1`

## Setup
In order to setup the server you must add a file creds.py, look ***creds.sample.py*** for example

- pip install -r req.txt
- flask run

We have managed the site with ngnix, and gunicorn in the production.

**We also had an admin panel to manage the site and user's data**
*[panel]()*