import json
from datetime import datetime, timedelta
from werkzeug import generate_password_hash, check_password_hash
from app import db
from .models import User

class DBModel():
    def __init__(self, db_model):
        self._model = db_model

    def get_all(self):
        return self._model.query.all()

    def get(self, item_id):
        return self._model.query.get(item_id)

    def get_items(self, item_ids):
        return self._model.query.filter(self._model.id.in_(item_ids)).all()

    def delete_all(self):
        db.session.query(self._model).delete()
        db.session.commit()

    def delete(self, item_id):
        db.session.query(self._model).delete(item_id)
        db.session.commit()
        
class UserPool(DBModel):
    def __init__(self):
        super().__init__(User)

    def add_user(self, user_data):
        new_user = User(
            id=user_data['email_id'],
            password=generate_password_hash(user_data['pwd']),
            role='student')
        db.session.add(new_user)
        db.session.commit()

    def check_password(self, user_id, password):
        user = self.get(user_id)
        return user and check_password_hash(user.password, password)

    def get_users_by_roles(self, roles):
        return self._model.query.filter(self._model.role.in_(roles)).all()
