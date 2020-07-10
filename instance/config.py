import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CLIENT_ID = '7535324'
REDIRECT_URI = 'https://emphasofttask.herokuapp.com/'
CLIENT_SECRET = 'v4jIc0UsD3SUf4sfovZR'

