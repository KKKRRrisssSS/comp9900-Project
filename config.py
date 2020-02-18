import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASEDIR, 'app', 'data')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATA_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
