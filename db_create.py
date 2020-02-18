import os, config
from app import db

os.remove(os.path.join(config.DATA_DIR, "app.db"))
db.create_all()