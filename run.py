from app import app
# import pyOpenSSL

if __name__=="__main__":
	app.run('0.0.0.0', port=5000, debug=True)