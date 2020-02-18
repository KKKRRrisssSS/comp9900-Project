from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

app = Flask(__name__)
app.secret_key = 'much_secret_very_key'
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

cred = credentials.Certificate("app/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db1 = firestore.client()

from .System import System
system = System()
from app import views_login, views_dashboard, authentication, views_userprofile