from app import db

class User(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(32), nullable=False)

    def __str__(self):
        return '<User {}>'.format(str(self.id))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


